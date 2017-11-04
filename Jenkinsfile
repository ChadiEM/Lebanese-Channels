pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Pylint') {
            steps {
                checkout scm
                sh 'python3 -m pylint --disable=C0111 --output-format=parseable lebanese_channels || exit 0'
            }
        }
        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                sh 'rsync -Crv ./ /opt/channels/ --delete'
                sh 'sudo /bin/systemctl restart channels.service'
            }
        }
    }
    post {
        always {
            warnings canComputeNew: false, canResolveRelativePaths: false, canRunOnFailed: true, categoriesPattern: '', consoleParsers: [[parserName: 'PyLint']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''
        }
    }
}
