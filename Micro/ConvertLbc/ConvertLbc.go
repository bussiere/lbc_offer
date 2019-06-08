package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"github.com/lib/pq"
	"strings"
	"time"
)




type RawOffer struct {
	RawOfferData string  `json:"Raw"`
	Modified      DateTime   `db:"Modified" json:"Modified"`
	Created       DateTime   `db:"Created" json:"Created"`
	Used sql.NullBool `db:"Used"`
}

type RawOfferLbc struct {
	RawOfferData string  `json:"RawOffer"`
	Modified      pq.NullTime    `db:"modified"`
	Created       pq.NullTime    `db:"created"`
}



func convertLbc(c *gin.Context) {
	var rawOffer RawOffer
	c.BindJSON(&rawOffer)
	fmt.Println(rawOffer.Created)
	var err error
	s := strings.Split(rawOffer.RawOfferData, `"ads": `)

	s2 := `{ "ads": ` + s[1]
	result := strings.Replace(s2, `, "status": "ready"}]`, ``, -1)
	//fmt.Println(result)
	var rawOfferLbc RawOfferLbc
	if err = json.Unmarshal([]byte(result), &rawOfferLbc); err != nil {
		fmt.Println(result)
		panic(err)
	}

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




