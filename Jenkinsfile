pipeline {
    agent any

    stages {
        stage('Initialize') {
            steps {
                // Initialize your build
                sh 'echo "Starting build..."'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                // Install any dependencies here
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Test') {
            steps {
                // Run your tests here
                sh 'echo "Running tests..."'
                // For example, you might run: sh 'pytest'
            }
        }

        stage('Build') {
            steps {
                // Build the package
                sh 'python setup.py sdist bdist_wheel'
            }
        }

        stage('Deploy') {
            steps {
                // Deploy the package              
                // This could be to a PyPI server, or any other target
                sh 'echo "Deploying package..."'
                sh 'twine upload dist/* --repository-url https://github.com/Jessicanyc/Generate-Dataframe'
            }
        }
    }

    post {
        always {
            // Post-build actions like cleanup, notifications, etc.
            sh 'echo "Build complete"'
        }
    }
}