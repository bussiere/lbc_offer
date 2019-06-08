package main

import (
	"fmt"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"github.com/lib/pq"
)




type RawOffer struct {
	RawOffer string  `json:"RawOffer"`
	Modified      pq.NullTime    `db:"modified"`
	Created       pq.NullTime    `db:"created"`
}




func convertLbc(c *gin.Context) {
	var rawOffer RawOffer
	c.BindJSON(&rawOffer)
	fmt.Println(rawOffer)

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




