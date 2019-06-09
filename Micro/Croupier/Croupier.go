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
	"sort"
	"time"

	"github.com/gin-gonic/gin"
)

type Pos struct {
	Geohash string `json:"Geohash"`
	NbMinute int `json:"NbMinute"`
}

type Response struct {
	Status        string  `json:"Status"`
	DistanceKm float64 `json:"DistanceKm"`
}

type Error struct {
	Message string `json:"Message"`
}

type GpsPos struct {
	GpsLat  float64 `json:"GpsLat"`
	GpsLong float64 `json:"GpsLong"`
}
type GeoHash struct {
	GeoHash  string `json:"GeoHash"`

}
type QueryData struct {
	PosOne GpsPos `json:"PosOne"`
	PosTwo GpsPos `json:"PosTwo"`
}

type QueryData2 struct {
	PosOne GeoHash `json:"PosOne"`
	PosTwo GeoHash `json:"PosTwo"`
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

}

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
	return km
}

func Process(query QueryData) Response {
	var response Response
	response.DistanceKm = Distance(query.PosOne.GpsLat, query.PosOne.GpsLong, query.PosTwo.GpsLat, query.PosTwo.GpsLong)
	response.Status = "Ok"
	return response

}
func Process2(query QueryData2) Response {
	var response Response
	lat1, lng1 := geohash.Decode(query.PosOne.GeoHash)
	lat2, lng2 := geohash.Decode(query.PosTwo.GeoHash)
	response.DistanceKm = Distance(lat1, lng1, lat2, lng2)
	response.Status = "Ok"
	return response

}


func CalculateDistance(c *gin.Context) {

	var query QueryData

	if c.BindJSON(&query) == nil {

		c.JSON(200, Process(query))
	} else {
		var errorInputData Error
		errorInputData.Message = "Incorrect input data"
		c.JSON(500, errorInputData)
	}

}
func CalculateDistanceHash(c *gin.Context) {

	var query QueryData2

	if c.BindJSON(&query) == nil {

		c.JSON(200, Process2(query))
	} else {
		var errorInputData Error
		errorInputData.Message = "Incorrect input data"
		c.JSON(500, errorInputData)
	}

}



func hsin(theta float64) float64 {
	return math.Pow(math.Sin(theta/2), 2)
}
func Distance(lat1, lon1, lat2, lon2 float64) float64 {
	// convert to radians
	// must cast radius as float to multiply later
	var la1, lo1, la2, lo2, r float64
	la1 = lat1 * math.Pi / 180
	lo1 = lon1 * math.Pi / 180
	la2 = lat2 * math.Pi / 180
	lo2 = lon2 * math.Pi / 180

	r = 6378100 // Earth radius in METERS

	// calculate
	h := hsin(la2-la1) + math.Cos(la1)*math.Cos(la2)*hsin(lo2-lo1)

	return 2 * r * math.Asin(math.Sqrt(h))
}


func getDistanceOffer {
	for _, station := range stations {
		var stationDistance StationDistance
		stationDistance.Station = station
		// response in kms
		stationDistance.DistanceFly = Distance(pos.GpsLat.Float64, pos.GpsLong.Float64, station.GpsLat.Float64, station.GpsLong.Float64) / 1000
		stationDistance.DistanceWalk = stationDistance.DistanceFly * flyCar
		stationDistance.TimeTravelWM = (stationDistance.DistanceWalk / walkSpeed)
		stationDistance.TimeTravelCM = (stationDistance.DistanceWalk / kmM)
		response.StationDistance = append(response.StationDistance, stationDistance)

	}
	sort.Slice(response.StationDistance, func(i, j int) bool {
		return response.StationDistance[i].DistanceFly < response.StationDistance[j].DistanceFly
	})
}


func getBuyFromHash(pos Pos) []OfferResponse {
	var query string
	var offers []OfferDB
	var err error
	query = `SELECT * FROM  "Offer_buy" WHERE geohash LIKE $1 || '%' AND available == TRUE ORDER BY date_ad`
	fmt.Println(query)
	err = db.Select(&offers, query,pos.Geohash[:4])
	if err != nil {
		panic(err)
	}
	var response []OfferResponse
	for _,offerDb := range offers {
		var offerR OfferResponse
		offerR.Geohash = offerDb.Geohash.String
		offerR.UrlOffer = offerDb.UrlOffer.String


		response = append(response,offerR)
	}
	return response
}

func getOfferFromHash(c *gin.Context) {
	var pos Pos
	var response Response
	c.BindJSON(&pos)
    var offers []OfferResponse
	offers = getBuyFromHash(pos)



	response.Status = "Ok"
	c.JSON(http.StatusOK, response)
}

var db *sqlx.DB
func main() {
	var err error
	db, err = sqlx.Connect("postgres", "user=admincomposcan dbname=offergreatparis password=KangourouIvre666 sslmode=disable")
	if err != nil {
		panic(err)
	}
	r := gin.Default()
	r.POST("/getOfferFromHash/", getOfferFromHash)
	r.Run(":8091") // listen and serve on 0.0.0.0:8080
}
