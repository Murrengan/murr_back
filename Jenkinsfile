CODE_CHANGES  = true

pipeline {
    agent any
    environment {
        NEW_VERSION = '0.0.135'
        SERVER_CREDENTIALS = credentials('ddddddddddddddddddddddddddddddddd')
        PWD = 11111
        USER = 11111
    }

    stages {
        stage('Build') {
            when {
                expression {
                    BRANCH_NAME == 'master' || CODE_CHANGES == true
                }
            }
            steps {
                echo 'Hello murrengan from build!'
            }
        }
        stage('Test') {
            when {
                expression {
                    BRANCH_NAME == 'develop'
                }
            }
            steps {
                echo 'Hello nyf-nyf'
                echo "Весия билда ${NEW_VERSION}"
                withCredentials([
                    usernamePassword(credentials: 'ddddddddddddddddddddddddddddddddd', usernameVariable: USER, passwordVariable: PWD)
                ]){
                    echo "${USER}  ${PWD}"
                    echo "murr-murr"
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
                echo 'SERVER_CREDENTIALS ${SERVER_CREDENTIALS}'
                sh "${SERVER_CREDENTIALS}"

            }
        }
    }
}
