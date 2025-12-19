const AWS = require("aws-sdk");

AWS.config.update({
  accessKeyId: process.env.AWS_KEY,
  secretAccessKey: process.env.AWS_SECRET,
  region: "ap-south-1"
});

const s3 = new AWS.S3();

async function uploadToS3(file) {
  const params = {
    Bucket: "forensic-evidence-bucket",
    Key: Date.now() + "_" + file.originalname,
    Body: file.buffer
  };

  const data = await s3.upload(params).promise();
  return data.Location; // Cloud URL
}

module.exports = uploadToS3;
