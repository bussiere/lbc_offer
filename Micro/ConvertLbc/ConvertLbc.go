package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	_	"github.com/lib/pq"
	"strings"
	"time"
)




type RawOffer struct {
	RawOfferData string  `json:"Raw"`
	Modified      time.Time   `db:"Modified" json:"Modified"`
	Created       time.Time  `db:"Created" json:"Created"`
	Used sql.NullBool `db:"Used"`
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
	
}

func convertLbc(c *gin.Context) {
	var rawOffer RawOffer
	c.BindJSON(&rawOffer)
	fmt.Println(rawOffer.RawOfferData)
	var err error
	s := strings.Split(rawOffer.RawOfferData, `"data": `)

	s2 := `{ "data": ` + s[1]
	result := strings.Replace(s2, `, "status": "ready"}]`, ``, -1)
	result = result + "}"
	fmt.Println(result)
	var rawOfferLbc RawOfferLbc
	if err = json.Unmarshal([]byte(result), &rawOfferLbc); err != nil {
		fmt.Println(result)
		panic(err)
	}
	fmt.Println(rawOfferLbc)

}


var db *sqlx.DB
func main() {
	var err error
	db, err = sqlx.Connect("postgres", "user=admincomposcan dbname=geomastermicro password=KangourouIvre666 sslmode=disable")
	if err != nil {
		panic(err)
	}
	fmt.Println("begin")
	r := gin.Default()
	r.Use(cors.Default())
	r.POST("/convertLbc/",convertLbc)
	r.Run((":8087"))
}




