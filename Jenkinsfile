pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Deploy Locally') {
            when {
                branch 'master'
            }
            steps {
                sh 'rsync -Crv ./ /opt/channels/ --delete'
                sh 'sudo /bin/systemctl restart channels.service'
            }
        }
    }
}
