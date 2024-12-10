import fs from "fs";
import xml2js from "xml2js";
export default function printStuff() {
  const { FIRST_NAME, LAST_NAME } = process.env;

  // read xml file
  const parser = new xml2js.Parser();
  fs.readFile(__dirname + "/reference.xml", function (err, data) {
    parser.parseString(data, function (err, result) {
      console.dir(result);
      console.log("Done");
    });
  });

  console.log(`Hello, ${FIRST_NAME} ${LAST_NAME}!`);
}
