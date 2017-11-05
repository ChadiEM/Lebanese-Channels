pipeline {
    agent none
    triggers {
        githubPush()
    }
    stages {
        stage('Pylint') {
            agent {
                dockerfile {
                    filename 'Dockerfile.build'
                }
            }
            steps {
                checkout scm
                sh 'pylint --disable=C0111 --persistent=no --output-format=parseable lebanese_channels > pylint.out || exit 0'
                warnings canComputeNew: false, canResolveRelativePaths: false, canRunOnFailed: true, categoriesPattern: '', parserConfigurations: [[parserName: 'PyLint', pattern: 'pylint.out']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''
            }
        }
        stage('Deploy') {
            agent any
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
