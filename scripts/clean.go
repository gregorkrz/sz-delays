package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
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

func ensureDir(path string) {
	if _, err := os.Stat(path); os.IsNotExist(err) {
		err := os.Mkdir(path, 0777)
		if err != nil {
			panic(err)
		}
	}
}

func dumpJson(data []Entry, filename string) {
	f, err := os.Create(filename)
	if err != nil {
		fmt.Println(err)
		return
	}
	out, err := json.Marshal(data)
	if err != nil {
		panic(err)
	}
	l, err := f.WriteString(string(out))
	if err != nil {
		fmt.Println(err)
		f.Close()
		return
	}
	fmt.Println(l, "bytes written successfully")
	err = f.Close()
	if err != nil {
		fmt.Println(err)
		return
	}
}

func main() {
	input_file := "data/raw/delayHistory.json"
	existing_trains := make(map[string]bool)
	jsonFile, err := os.Open(input_file)
	if err != nil {
		panic(err)
	}
	byteValue, _ := ioutil.ReadAll(jsonFile)
	var data []Entry
	json.Unmarshal(byteValue, &data)
	n := 0
	for _, v := range data {
		if v.Ts != 0 {
			data[n] = v
			for _, delay := range v.Delays {
				existing_trains[delay.TrainNo] = true
			}
			n++
		}
	}
	data = data[:n]

	fmt.Println("Data length:", len(data))
	out_dir := "data/processed"
	ensureDir(out_dir)
	dumpJson(data, filepath.Join(out_dir, "cleaned.json"))
}
