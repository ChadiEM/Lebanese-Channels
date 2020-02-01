#!/usr/bin/env groovy

pipeline {
    agent none

    stages {
        stage('Validate') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    additionalBuildArgs '--target lint'
                }
            }
            steps {
                sh 'python -m unittest discover -v tests'
                sh 'pylint --exit-zero --disable=C0111,C0301 --persistent=no --output-format=parseable lebanese_channels > pylint.out'
            }
            post {
                always {
                    warnings canComputeNew: false, canResolveRelativePaths: false, canRunOnFailed: true, categoriesPattern: '', parserConfigurations: [[parserName: 'PyLint', pattern: 'pylint.out']], defaultEncoding: '', excludePattern: '', healthy: '', includePattern: '', messagesPattern: '', unHealthy: ''
                }
            }
        }
    }
}
