const fs = require('fs');
const path = require('path');
const dir = path.resolve("files");
let finalContent = { "result": [] };

const usernames = [];
const read_directory = async dir =>
  fs.readdirSync(dir).reduce((finalContent, file) => {
    filePath = path.join(dir, file);
    let content = require(filePath);
    finalContent.result = finalContent.result.concat(content.result);
    content.result.forEach(profile => {
      if (!usernames.includes(profile.basic.username)) {
        usernames.push(profile.basic.username);
      }
    })
    return finalContent;
  }, { "result": [] });

read_directory(dir).then(data => {
  //combine all the json files that contain data about the influencers.
  fs.writeFileSync('./final.json', JSON.stringify(data));
  //extract the usernames of influencers for later to web scrape the public data from Instagram.
  console.log("Amount of users scrapped: ", usernames.length);
  fs.writeFileSync('./usernames.json', JSON.stringify(usernames));
});