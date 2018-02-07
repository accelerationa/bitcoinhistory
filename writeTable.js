const getJSON = require('get-json')
const fs = require('fs')
const path = require('path')
const chalk = require('chalk')
const figlet = require('figlet')
var AWS = require('aws-sdk')

const outputFile = process.argv.slice(2)[0]
const dataDir = 'data/'

console.log(chalk.green(figlet.textSync('Bitcoin Chart Scraper', {
	font: 'Pepper',
	kerning: 'fitted'
})))
console.log(chalk.dim(`Combining data to=${chalk.yellow(outputFile)} \n`))

const files = []

function compare (a, b) {
	if (a.time < b.time) {
		return -1
	}

	if (a.time > b.time) {
		return 1
	}

	return 0
}

fs.readdir(dataDir, (err, list) => {
	list.forEach(file => {
		let date
		let time

		try {
			date = new Date(file.split('bitstampUSD-')[1].split('.json')[0])
			time = date.getTime()
		} catch (err) {
			return
		}

		if (!date) {
			return
		}

		files.push({
			file,
			date,
			time
		})
	})

	files.sort(compare)

	let combinedData = []

	process.stdout.write('\n')

	files.forEach(day => {
		const filePath = path.join(dataDir, day.file)
		const contents = fs.readFileSync(path.join(__dirname, filePath)).toString()
		const data = JSON.parse(contents)

		
		data.forEach(col => {
			var item = {
				'Time': col[0],
				'Open': col[1],
				'High': col[2],
				'Low': col[3],
				'Close': col[4],
				'Volumn_BTC': col[5],
				'Volumn_Currency': col[6],
				'Weighted_Price': col[7]
			}
			writeDDB(item)
		})

		process.stdout.write('.')
	})

	const outputData = JSON.stringify(combinedData)
})


function writeDDB(item) {
	
	AWS.config.update({
		region: "us-east-2",
		endpoint: "http://localhost:8080"
	  });
	  
	  var docClient = new AWS.DynamoDB.DocumentClient();
	  
	  var table = "BitcoinHistoryData";
	  
	  var params = {
		  TableName:table,
		  Item: item
	  };

	  
	  docClient.put(params, function(err, data) {
		  if (err) {
			  console.error("Unable to add item. Error JSON:", JSON.stringify(err, null, 2));
		  } else {
			  console.log("Added item:", JSON.stringify(data, null, 2));
		  }
	  });
}