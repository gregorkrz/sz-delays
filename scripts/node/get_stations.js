import request from "./soap_client"
const fs = require('fs');

const out_file 
request("Postaje").then( r => {
    console.log("Successfully fetched station data");
})

// directory to check if exists
const dir = 'data/';

// check if directory exists
if (fs.existsSync(dir)) {
    console.log('Directory exists!');
} else {
    console.log('Directory not found.');
}