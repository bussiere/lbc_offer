package main

import (
	"database/sql"
	"fmt"
	"github.com/jmoiron/sqlx"
	"github.com/lib/pq"
	"github.com/mmcloughlin/geohash"
	"github.com/umahmood/haversine"
	"math"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type Pos struct {
	Geohash string `json:"Geohash"`
	NbMinuteCar int `json:"NbMinuteCar"`
	NbMinuteWalk int `json:"NbMinuteWalk"`
}

type Response struct {
	Status        string  `json:"Status"`
	Offers []OfferResponse `json:"Offers"`
}

type Error struct {
	Message string `json:"Message"`
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

type OfferResponse struct {
	Id          int             `json:"id"`
	Uuid        string  `json:"uuid"`
	Name        string `json:"name"`
	Geohash     string  `json:"geohash"`
	GpsLat      float64 `json:"gps_lat"`
	GpsLong      float64 `json:"gps_long"`
	CatOne      string  `json:"cat_one"`
	DateAd      time.Time     `json:"date_ad"`
	M2          int64   `json:"m2"`
	UrlOffer    string `json:"url_offer"`
	Description string `json:"description"`
	Piece       int64  `json:"piece"`
	Available   bool            `json:"available"`
	Price       float64 `json:"price"`
	Seller      string  `json:"seller"`
	Commune     string  `json:"commune"`
	PostalCode  string `json:"postal_code"`
	Pic1        string   `json:"pic1"`
	Type string   `json:"Type"`
	DistanceFly  float64 `json:"DistanceFly"`
	DistanceCar float64 `json:"DistanceCar"`
	TimeTravelWM  float64 `json:"TimeTravelWM"`
	TimeTravelCM  float64 `json:"TimeTravelCM"`
	UrlMap    string `json:"TimeTravelCM"`

}

// Todo adding seller selection

// haversin(?) function
func hsin(theta float64) float64 {
	return math.Pow(math.Sin(theta/2), 2)
}

// Distance function returns the distance (in meters) between two points of
// a given longitude and latitude relatively accurately (using a spherical
// approximation of the Earth) through the Haversin Distance Formula for
// great arc distance on a sphere with accuracy for small distances
//
// point coordinates are supplied in degrees and converted into rad. in the func
//
// distance returned is METERS!!!!!!
// http://en.wikipedia.org/wiki/Haversine_formula
func Distance(lat1, lon1, lat2, lon2 float64) float64 {
	// convert to radians
	// must cast radius as float to multiply later
	point1 := haversine.Coord{Lat: lat1, Lon: lon1}  // Oxford, UK
	point2  := haversine.Coord{Lat: lat2, Lon: lon2}  // Turin, Italy
	_, km := haversine.Distance(point1, point2)
	km = km/1000
	return km
}







func getDistanceOffer (pos Pos,offers *[]OfferResponse){
	posGpsLat,posGpsLong := geohash.Decode(pos.Geohash)
	for index, offer := range *offers  {
		offer.DistanceFly = Distance(posGpsLat, posGpsLong, offer.GpsLat, offer.GpsLong)
		offer.DistanceCar = offer.DistanceFly * flyCar
		offer.TimeTravelWM = (offer.DistanceCar  / walkSpeed)
		offer.TimeTravelCM = (offer.DistanceCar  / kmM)
		(*offers)[index] = offer
	}
}


func getBuyFromHash(pos Pos,response *[]OfferResponse) {
	var query string
	var err error
	var offers []OfferDB
	query = `SELECT * FROM  "Offer_buy" WHERE geohash LIKE $1 || '%' AND available ORDER BY date_ad`
	fmt.Println(query)
	err = db.Select(&offers, query, pos.Geohash[:4])
	if err != nil {
		panic(err)
	}
	for _, offerDb := range offers {
		var offerR OfferResponse
		offerR.Geohash = offerDb.Geohash.String
		offerR.UrlOffer = offerDb.UrlOffer.String
		offerR.Price = offerDb.Price.Float64
		offerR.Uuid = offerDb.Uuid.String
		offerR.Pic1 = offerDb.Pic1.String
		offerR.GpsLat = offerDb.GpsLat.Float64
		offerR.GpsLong = offerDb.GpsLong.Float64
		offerR.Description = offerDb.Description.String
		offerR.PostalCode = offerDb.PostalCode.String
		offerR.Commune = offerDb.Commune.String
		offerR.DateAd = offerDb.DateAd.Time
		offerR.M2 = offerDb.M2.Int64
		offerR.Piece = offerDb.Piece.Int64
		offerR.Seller = "LBC"
		*response = append(*response, offerR)
	}
}

func sortTime(pos Pos,offers *[]OfferResponse){
	for index,offer := range *offers {
		if (int(offer.TimeTravelCM) > pos.NbMinuteCar && int(offer.TimeTravelWM) > pos.NbMinuteWalk) {
			*offers = append((*offers)[:index], (*offers)[index+1:]...)
		}
	}
}


func getOfferFromHash(c *gin.Context) {
	var pos Pos
	var response Response
	c.BindJSON(&pos)
    var offers []OfferResponse
	getBuyFromHash(pos,&offers)
	getDistanceOffer(pos,&offers)
	sortTime(pos,&offers)


    response.Offers = offers
	response.Status = "Ok"
	c.JSON(http.StatusOK, response)
}


var db *sqlx.DB
var kmM float64
var flyCar float64
var walkSpeed float64
func main() {
	kmM = (0.026480)*60
	flyCar = 1.502274
	walkSpeed = (0.00125)*60
	var err error
	db, err = sqlx.Connect("postgres", "user=admincomposcan dbname=offergreatparis password=KangourouIvre666 sslmode=disable")
	if err != nil {
		panic(err)
	}
	r := gin.Default()
	r.POST("/getOfferFromHash/", getOfferFromHash)
	r.Run(":8091") // listen and serve on 0.0.0.0:8080
}
