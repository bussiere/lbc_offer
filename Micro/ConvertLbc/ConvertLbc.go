package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"
	"github.com/lib/pq"
	_ "github.com/lib/pq"
	"github.com/mmcloughlin/geohash"
	"golang.org/x/text/transform"
	"golang.org/x/text/unicode/norm"
	"strconv"
	"strings"
	"time"
	"unicode"
)

type RawOffer struct {
	RawOfferData string       `json:"Raw"`
	Modified     time.Time    `db:"Modified" json:"Modified"`
	Created      time.Time    `db:"Created" json:"Created"`
	Used         sql.NullBool `db:"Used"`
}

type RawOfferLbc struct {
	Data struct {
		Total         int    `json:"total"`
		TotalAll      int    `json:"total_all"`
		TotalPro      int    `json:"total_pro"`
		TotalPrivate  int    `json:"total_private"`
		TotalActive   int    `json:"total_active"`
		TotalInactive int    `json:"total_inactive"`
		Pivot         string `json:"pivot"`
		Ads           []struct {
			ListID               int         `json:"list_id"`
			FirstPublicationDate string      `json:"first_publication_date"`
			ExpirationDate       string      `json:"expiration_date"`
			IndexDate            string      `json:"index_date"`
			Status               string      `json:"status"`
			CategoryID           string      `json:"category_id"`
			CategoryName         string      `json:"category_name"`
			Subject              string      `json:"subject"`
			Body                 string      `json:"body"`
			AdType               string      `json:"ad_type"`
			URL                  string      `json:"url"`
			Price                []int       `json:"price"`
			PriceCalendar        interface{} `json:"price_calendar"`
			Images               struct {
				ThumbURL  string   `json:"thumb_url"`
				SmallURL  string   `json:"small_url"`
				NbImages  int      `json:"nb_images"`
				Urls      []string `json:"urls"`
				UrlsThumb []string `json:"urls_thumb"`
				UrlsLarge []string `json:"urls_large"`
			} `json:"images"`
			Attributes []struct {
				Key        string `json:"key"`
				Value      string `json:"value"`
				KeyLabel   string `json:"key_label,omitempty"`
				ValueLabel string `json:"value_label"`
				Generic    bool   `json:"generic"`
			} `json:"attributes"`
			Location struct {
				RegionID       string  `json:"region_id"`
				RegionName     string  `json:"region_name"`
				DepartmentID   string  `json:"department_id"`
				DepartmentName string  `json:"department_name"`
				CityLabel      string  `json:"city_label"`
				City           string  `json:"city"`
				Zipcode        string  `json:"zipcode"`
				Lat            float64 `json:"lat"`
				Lng            float64 `json:"lng"`
				Source         string  `json:"source"`
				Provider       string  `json:"provider"`
				IsShape        bool    `json:"is_shape"`
			} `json:"location"`
			Owner struct {
				StoreID    string `json:"store_id"`
				UserID     string `json:"user_id"`
				Type       string `json:"type"`
				Name       string `json:"name"`
				NoSalesmen bool   `json:"no_salesmen"`
			} `json:"owner"`
			Options struct {
				HasOption  bool `json:"has_option"`
				Booster    bool `json:"booster"`
				Photosup   bool `json:"photosup"`
				Urgent     bool `json:"urgent"`
				Gallery    bool `json:"gallery"`
				SubToplist bool `json:"sub_toplist"`
			} `json:"options"`
			HasPhone bool `json:"has_phone"`
		} `json:"ads"`
	} `json:"data"`
}

type OfferDB struct {
	Id          int             `db:"id"`
	Modified    pq.NullTime     `db:"modified"`
	Created     pq.NullTime     `db:"created"`
	Uuid        sql.NullString  `db:"uuid"`
	AdId        sql.NullInt64   `db:"ad_id"`
	Name        sql.NullString  `db:"name"`
	Geohash     sql.NullString  `db:"geohash"`
	GpsLat      sql.NullFloat64 `db:"gps_lat"`
	GpsLong     sql.NullFloat64 `db:"gps_long"`
	CatOne      sql.NullString  `db:"cat_one"`
	CatTwo      sql.NullString  `db:"cat_two"`
	DateAd      pq.NullTime     `db:"date_ad"`
	M2          sql.NullInt64   `db:"m2"`
	M2Bis       sql.NullInt64   `db:"m2_1"`
	AdresseUuid sql.NullString  `db:"adresse_uuid"`
	UrlOffer    sql.NullString  `db:"url_offer"`
	Note        sql.NullString  `db:"note"`
	Description sql.NullString  `db:"description"`
	Piece       sql.NullInt64   `db:"piece"`
	Chambre     sql.NullInt64   `db:"chambre"`
	Available   bool            `db:"available"`
	Price       sql.NullFloat64 `db:"price"`
	Ref1        sql.NullString  `db:"ref1"`
	Ref2        sql.NullString  `db:"ref2"`
	Score       sql.NullInt64   `db:"score"`
	Origin      sql.NullString  `db:"origin"`
	SellerId    sql.NullInt64   `db:"seller_id"`
	Commune     sql.NullString  `db:"commune"`
	PostalCode  sql.NullString  `db:"postal_code"`
	Pic1        sql.NullString  `db:"pic1"`
}

type Seller struct {
	Id          int             `db:"id"`
	GroupeId sql.NullInt64 `db:"group_id"`
	Modified    pq.NullTime     `db:"modified"`
	Created     pq.NullTime     `db:"created"`
	Uuid        sql.NullString  `db:"uuid"`
	Name        sql.NullString  `db:"name"`
	AdresseUuid sql.NullString  `db:"adresse_uuid"`
	Geohash     sql.NullString  `db:"geohash"`
	GpsLat      sql.NullFloat64 `db:"gps_lat"`
	GpsLong     sql.NullFloat64 `db:"gps_long"`
	Url sql.NullString  `db:"url"`
	Contact sql.NullString `db:"contact"`
	Phone sql.NullString `db:"phone"`
	Email sql.NullString `db:"email"`
	Note sql.NullString `db:"note"`
}

func convertLbc(c *gin.Context) {
	var rawOffer RawOffer
	c.BindJSON(&rawOffer)
	//fmt.Println(rawOffer.RawOfferData)
	var err error
	s := strings.Split(rawOffer.RawOfferData, `"data": `)

	s2 := `{ "data": ` + s[1]
	result := strings.Replace(s2, `, "status": "ready"}]`, ``, -1)
	result = result + "}"
	//fmt.Println(result)
	var rawOfferLbc RawOfferLbc
	if err = json.Unmarshal([]byte(result), &rawOfferLbc); err != nil {
		//fmt.Println(result)
		panic(err)
	}
	DecodeRaw(rawOfferLbc)
	//fmt.Println(rawOfferLbc)

}

func DecodeRaw(rawOfferLbc RawOfferLbc) {

	var query string
	query = `SELECT * FROM  "Offer_buy" WHERE ad_id=$1`

	fmt.Println("inside convert")
	var keyMeter int
	var keyRoom int
	var keyType int
	for _, ad := range rawOfferLbc.Data.Ads {
		var offerDB OfferDB
		var offers []OfferDB

		if ad.CategoryName == "Ventes immobili\u00e8res" && len(ad.Price) == 1 && ad.Price[0] > 10000 {
			err := db.Select(&offers, query, ad.ListID)
			if err != nil {
				panic(err)
			}
			if len(offers) ==  0 {

				offerDB.AdId.Int64 = int64(ad.ListID)
				offerDB.AdId.Valid = true

				offerDB.UrlOffer.String = ad.URL
				offerDB.UrlOffer.Valid = true

				offerDB.Origin.String = "lbc_db"
				offerDB.Origin.Valid = true

				offerDB.Uuid.String = uuid.New().String()
				offerDB.Uuid.Valid = true

				offerDB.Created.Time = time.Now()
				offerDB.Created.Valid = true

				offerDB.Name.String = ad.Subject
				offerDB.Name.Valid = true

				offerDB.DateAd.Time, err = time.Parse("2006-01-02 15:04:05", ad.FirstPublicationDate)
				if err != nil {
					panic(err)
				}
                fmt.Println(ad.Price)
				offerDB.Price.Float64 = float64(ad.Price[0])
				offerDB.Price.Valid = true

				// the key for the m2

				keyRoom = -1
				keyType = -1
				keyMeter = -1
				for index, attribute := range ad.Attributes {
					if attribute.Key == "square" {
						keyMeter = index
					}
					if attribute.Key == "rooms" {
						keyRoom = index
					}

					if (attribute.ValueLabel == "Maison" || attribute.ValueLabel == "Appartement" || attribute.ValueLabel == "Terrain" ){
						keyType = index
					}
				}
				if (keyType == -1 || keyRoom == -1 || keyMeter == -1 ){
					return
				}

				offerDB.CatOne.String = ad.Attributes[keyType].ValueLabel
				offerDB.CatOne.Valid = true

				offerDB.M2.Int64, err = strconv.ParseInt(ad.Attributes[keyMeter].Value, 10, 64)
				if err != nil {
					//panic(err)
					return
				}

				offerDB.M2.Valid = true

				if keyRoom != - 1 {
					offerDB.Piece.Int64, err = strconv.ParseInt(ad.Attributes[keyRoom].Value, 10, 64)
					if err != nil {
						//panic(err)
						return
					}

					offerDB.Piece.Valid = true
				} else {
					return
				}
				// location block
				offerDB.Commune.String = ad.Location.City
				offerDB.Commune.Valid = true

				offerDB.PostalCode.String = ad.Location.Zipcode
				offerDB.PostalCode.Valid = true

				offerDB.GpsLat.Float64 = ad.Location.Lat
				offerDB.GpsLat.Valid = true
				offerDB.GpsLong.Float64 = ad.Location.Lng
				offerDB.GpsLong.Valid = true
				offerDB.Geohash.String = geohash.Encode(offerDB.GpsLat.Float64, offerDB.GpsLong.Float64)
				offerDB.Geohash.Valid = true


				// description
				if len(ad.Body) > 800 {
					ad.Body = ad.Body[:799]
				}
				offerDB.Description.String = RemoveAccent(ad.Body)
				offerDB.Description.Valid = true

				offerDB.Pic1.String = ad.Images.ThumbURL
				offerDB.Pic1.Valid = true





				offerDB.Available = true
				tx := db.MustBegin()
				if err != nil {
					panic(err)
				}
				//tx.NamedExec(`INSERT INTO "Offer_buy" (ad_id, date_ad, price,cat_one,m2,piece,commune,postal_code,gps_lat,gps_long,geohash,description,pic1) VALUES (:ad_id, :date_ad, :price,:m2,:piece,:commune,:postal_code,:gps_lat,:gps_long,:geohash,:description,:pic1)`, offerDB)
				//TODO :  need to optimize
				tx.MustExec(`INSERT INTO "Offer_buy"  (ad_id,available,seller_id,name,piece,m2,price,cat_one,date_ad,commune,postal_code,gps_lat,gps_long,geohash,description,pic1,uuid,url_offer,origin,created) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20)`, offerDB.AdId,true,lbc.Id,offerDB.Name,offerDB.Piece,offerDB.M2,offerDB.Price,offerDB.CatOne,offerDB.DateAd,offerDB.Commune,offerDB.PostalCode,offerDB.GpsLat,offerDB.GpsLong,offerDB.Geohash,offerDB.Description,offerDB.Pic1,offerDB.Uuid,offerDB.UrlOffer,offerDB.Origin,offerDB.Created)

				err = tx.Commit()
				if err != nil {
					panic(err)
				}
				fmt.Println("inserted in db normally ...")
			}
		}
	}

}

func Test() {
	var query string
	var offers []OfferDB
	var sellers []Seller
	var err error
	var test string
	test = uuid.New().String()
	fmt.Println(test)
	query = `SELECT * FROM  "Offer_buy" WHERE id=$1`
	err = db.Select(&offers, query, 1)
	if err != nil {
		panic(err)
	}
	fmt.Println(offers)
//	fmt.Println(offers[0].Geohash)
	query = `SELECT * FROM  "Offer_seller" WHERE id=$1`
	err = db.Select(&sellers, query, 1)
	if err != nil {
		panic(err)
	}
	fmt.Println(sellers)

}

func isMn(r rune) bool {
	return unicode.Is(unicode.Mn, r) // Mn: nonspacing marks
}
func RemoveAccent(name string) string{
	t := transform.Chain(norm.NFD, transform.RemoveFunc(isMn), norm.NFC)
	result, _, _ := transform.String(t, name)
	return result
}

func InitSeller() {
	var seller Seller
	var sellers []Seller
	var err error
	seller.Name.String = "lbc"
	seller.Name.Valid = true
	var query string
	query = `SELECT * FROM  "Offer_seller" WHERE name=$1`
	err = db.Select(&sellers, query, seller.Name)
	if err != nil {
		panic(err)
	}
	if len(sellers) == 0 {
		tx := db.MustBegin()
		tx.MustExec(`INSERT INTO "Offer_seller"  (name) VALUES ($1)`, seller.Name)

		err = tx.Commit()
		if err != nil {
			panic(err)
		}
		query = `SELECT * FROM  "Offer_seller" WHERE name=$1`
		err = db.Select(&sellers, query, seller.Name)
		if err != nil {
			panic(err)
		}
		lbc = sellers[0]

	} else {
		lbc = sellers[0]
	}

}
var db *sqlx.DB
var lbc Seller
func main() {
	var err error
	db, err = sqlx.Connect("postgres", "user=admincomposcan dbname=offergreatparis password=KangourouIvre666 sslmode=disable")
	if err != nil {
		panic(err)
	}
	Test()
	InitSeller()
	fmt.Println("begin")
	r := gin.Default()
	r.Use(cors.Default())
	r.POST("/convertLbc/", convertLbc)
	r.Run((":8087"))
}
