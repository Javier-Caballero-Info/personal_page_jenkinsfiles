node {
    stage('Preparation') {
        currentBuild.displayName = "Build_" + "${BUILD_TIMESTAMP}"
        git 'git@github.com:Javier-Caballero-Info/personal_page_authenticator_python.git'
    }
    stage('Docker build'){
        sh '/usr/local/bin/docker build -t javiercaballeroinfo/personal_page_authenticator_python:$Docker_Tag .'
    }
    stage('Docker push'){
        sh '/usr/local/bin/docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
        sh '/usr/local/bin/docker push javiercaballeroinfo/personal_page_authenticator_python:$Docker_Tag'
    }
    stage('Update Deployer Manager'){
        httpRequest acceptType: 'APPLICATION_JSON', contentType: 'APPLICATION_JSON', customHeaders: [[maskValue: false, name: 'Authorization', value: 'Basic Y2FiYWxsZXJvamF2aWVyMTNAZ21haWwuY29tOkxpbmtpbiQxMw==']], httpMode: 'PUT', responseHandle: 'NONE', url: 'http://deployer.javiercaballero.info/api/v1/app_versions?app_id=5b843fa371531a000612d165', validResponseCodes: '202'
    }
}