export default function printStuff() {
  const { FIRST_NAME, LAST_NAME } = process.env;

  console.log(`Hello ${FIRST_NAME} ${LAST_NAME}`);
  console.log("stuff");
}
