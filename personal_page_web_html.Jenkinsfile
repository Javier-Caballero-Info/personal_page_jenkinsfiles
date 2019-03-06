node {
    stage('Preparation') {
        currentBuild.displayName = "Build_" + "${BUILD_TIMESTAMP}"
        git 'git@github.com:Javier-Caballero-Info/personal_page_web_html.git'
    }
    stage('Installing dependencies'){
        nodejs('Node10.15.0') {
            sh 'npm install'
        }
    }
    stage('Npm Build'){
        nodejs('Node10.15.0') {
            sh 'npm run build'
        }
    }
    stage('Docker build'){
        sh '/usr/local/bin/docker build -t javiercaballeroinfo/personal_page_web_html:$Docker_Tag .'
    }
    stage('Docker push'){
        sh '/usr/local/bin/docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
        sh '/usr/local/bin/docker push javiercaballeroinfo/personal_page_web_html:$Docker_Tag'
    }
    stage('Update Deployer Manager'){
        httpRequest acceptType: 'APPLICATION_JSON', contentType: 'APPLICATION_JSON', customHeaders: [[maskValue: false, name: 'Authorization', value: 'Basic Y2FiYWxsZXJvamF2aWVyMTNAZ21haWwuY29tOkxpbmtpbiQxMw==']], httpMode: 'PUT', responseHandle: 'NONE', url: 'http://deployer.javiercaballero.info/api/v1/app_versions?app_id=5b84416471531a000612d16b', validResponseCodes: '202'
    }
}