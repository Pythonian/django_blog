# Setup Sass styling

* npm init -y
* npm install node-sass // node-sass compiles .scss files to css
* npm install browser-sync
* npm run sass // Run the sass watch script
* npm run sync // Run the BrowserSync
* Open the link http://localhost:3000/ to watch for file changes

# Setup Amazon S3 Storage and CloudFront

* Visit https://aws.amazon.com/ and create an account
* Visit the Services section and click the S3 link
* Create a new bucket
* Uncheck the Block public access option and press Create bucket
* Visit the Services section and click IAM under the Security, Identity & Compliance label
* Click Users and Add user
* In Access type, check Programmatic access
* Hit Next: permissions and Create a new group; Check AmazonS3FullAccess
* Click Next: Tags; Click Next: Review; Click Create user
* Use the Access key ID and Secret access key in the settings.py file
* Click Close the at the bottom and Visit Services > S3 and click your bucket name
* Navigate to Permissions > Bucket Policy and add the following:
``
{
    "Version": "2012-10-17",
    "Id": "Policy1545746178921",
    "Statement": [
        {
            "Sid": "Stmt1545746153677",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::bucket-name/*"
        }
    ]
}
``

# Setup Amazon CloudFront CDN
* Visit Services and search for cloudfront
* Click Create Distribution
* Click Get Started to create a web distribution
* Select your bucket as the Origin Domain Name
* Scroll down to the bottom and click Create Distribution
* Wait until the distribution is deployed


# Creating a Heroku pipeline

* Visit your Heroku app Deploy page and create a pipeline
* Name the pipeline and choose a stage to add your app to
* Connect to Github
* Visit the Pipeline page and Enable Automatic Deploys

## Adding a Production app to Heroku pipeline

* Visit the Pipeline page and add a Production app
* Press your staging app Promote to production button

## Enabling review apps

* Visit the Pipeline page and press Enable Review Apps
* Create an app.json file
* Click on Commit to Repo button
* Check Create new review apps…automatically and Destroy stale review apps