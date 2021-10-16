package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/globusdigital/soap"
)

func ensureDir(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.Mkdir(path, 0777)
		if err != nil {
			panic(err)
		}
	}
}

type FooRequest struct {
	Username string `xml:"username"`
	Password string `xml:"password"`
}

type Postaja struct {
	St    string `xml:"st"`
	Naziv string `xml:"naziv"`
	Lat   string `xml:"Geo_sirina"`
	Lng   string `xml:"Geo_dolzina"`
}

func main() {
	apiEndpoint := "http://91.209.49.139/webse/se.asmx"
	client := soap.NewClient(apiEndpoint, nil)
	var resp []Postaja
	params := FooRequest{
		Username: "zeljko",
		Password: "joksimovic",
	}

	res, err := client.Call(context.TODO(), "Postaje", &params, &resp)
	if err != nil {
		log.Fatalf("Call error: %s", err)
	}

	fmt.Println(res)
}
