package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"time"

	"github.com/jackc/pgx"
)

type Entry struct {
	Ts     int           `json:"_id"`
	Delays []DelayRecord `json:"delays"`
}

type DelayRecord struct {
	Rte         string `json:"route"`
	TrainNo     string `json:"trainnumber"`
	Stn         string `json:"station"`
	Delay       int    `json:"delay"`
	TypeOfDelay int    `json:"typeofdelay"`
}

func loadFeed(data []Entry) {
	connString := fmt.Sprintf("postgres://%s:%s@%s:%s/%s", "root", "example", "localhost", "5432", "postgres")
	conn, err := pgx.Connect(context.Background(), connString)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())
	fmt.Println("inserting into database")
	batch := &pgx.Batch{}
	//bs := 10000
	commit := func() {
		br := conn.SendBatch(context.Background(), batch)
		_, err = br.Exec()
		if err != nil {
			panic(err)
		}
		batch = &pgx.Batch{}
		br.Close()
	}
	for _, d := range data {
		//if n%bs == 0 && batch.Len() > 0 {
		//	commit()
		//}
		ts := time.Unix(int64(d.Ts), 0)
		for _, delay := range d.Delays {
			batch.Queue("insert into sz_zamude.feed(ts, train, line, station, delay, delaytype) values ($1, $2, $3, $4, $5, $6)",
				ts, delay.TrainNo, delay.Rte, delay.Stn, delay.Delay, delay.TypeOfDelay)
		}
	}
	if batch.Len() > 0 {
		commit()
	}
	fmt.Println("inserted")
}

func main() {

	filepath := "../data/raw/delayHistory.json"
	jsonFile, err := os.Open(filepath)
	if err != nil {
		fmt.Println(err)
	}
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var data []Entry
	json.Unmarshal(byteValue, &data)
	n := 0
	for _, v := range data {
		if v.Ts != 0 {
			data[n] = v
			n++
		}
	}
	data = data[:n]
	for _, d := range data {
		for _, i := range d.Delays {
			_, err := strconv.Atoi(i.TrainNo)
			if err != nil {
				fmt.Println(i.TrainNo)
			}
		}

	}
	fmt.Println("Data length:", len(data))

	loadFeed(data)
}
