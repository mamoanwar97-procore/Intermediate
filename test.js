const fs = require("fs");
const { execSync } = require("child_process");
const xml2js = require("xml2js");

const parentDir = process.cwd();
const defaultCollectionBranch = "translations-collection";

const gitToken = process.env.GITHUB_TOKEN;
const gitUrl = process.env.GIT_ORIGIN_URL;
const gitRef = process.env.GIT_HEAD_REF;
console.log(gitToken);
console.log(gitUrl);
console.log(gitRef);

// Parse the XML file
const xmlData = fs.readFileSync(`${parentDir}/reference.xml`, "utf8");
xml2js.parseString(xmlData, (err, result) => {
  if (err) {
    throw err;
  }

  execSync(`git remote set-url origin ${gitUrl}`);
  execSync(`git checkout origin/${defaultCollectionBranch}`);
  execSync("git config pull.rebase false");

  // Loop over the project elements in the XML file
  const projects = result.manifest.project;
  projects.forEach((project) => {
    const repo = project.$.name;
    const revision = project.$.revision || "main"; // This is optional, default to 'main'
    const branch = project.$.branch;
    console.log("repo", repo, revision, branch);

    // create new branch to collect all translations updates from all repos
    // execSync(`git pull origin ${branch}`);
  });

  //   execSync(`git push origin ${defaultCollectionBranch}`);
  //   execSync(
  //     'gh pr create --base main --head translations-collection --title "Translations Update" --body "Translations Update"'
  //   );
});
