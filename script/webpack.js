const configPath = process.argv[2];
const config = require(configPath);
console.log(JSON.stringify(config.resolve));
