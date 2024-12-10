import fs from "fs";
import { execSync } from "child_process";
import { parseString } from "xml2js";

// Get the current working directory (repository root)
const parentDir = process.cwd();

// Read the XML file
const xmlData = fs.readFileSync(`${parentDir}/reference.xml`, "utf8");

// Parse the XML data
parseString(xmlData, (err, result) => {
  if (err) {
    console.error("Error parsing XML:", err);
    process.exit(1);
  }

  const projects = result.manifest.project;
  console.log("Found", projects.length, "projects to process.");

  projects.forEach((project) => {
    const repoName = project.$.name;
    const branch = project.$.branch || "main"; // Default to 'main' if no branch is specified
    const filePath = project.$.file; // File path to copy from the repo

    console.log(
      `Processing ${repoName} on branch ${branch}, file: ${filePath}`
    );

    try {
      // Clone the repo with the specified branch
      const repoDir = `${parentDir}/${repoName}`;

      execSync(
        `git clone --branch ${branch} https://github.com/${repoDir}.git`,
        { stdio: "inherit" }
      );

      // Navigate into the cloned repo
      const fileToCopy = `${repoDir}/${filePath}`;
      const destDir = `${parentDir}/collected-files`; // Destination folder to store files

      // Ensure the destination directory exists
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir);
      }

      // Copy the specified file to the action repository
      if (fs.existsSync(fileToCopy)) {
        const fileName = filePath.split("/").pop(); // Extract the file name
        fs.copyFileSync(fileToCopy, `${destDir}/${fileName}`);
        console.log(`Copied ${fileToCopy} to ${destDir}/${fileName}`);
      } else {
        console.error(
          `File ${fileToCopy} does not exist in repository ${repoName}`
        );
      }

      // Clean up the cloned repo
      fs.rmdirSync(repoDir, { recursive: true });
    } catch (error) {
      console.error(`Error processing repository ${repoName}:`, error);
    }
  });
});
