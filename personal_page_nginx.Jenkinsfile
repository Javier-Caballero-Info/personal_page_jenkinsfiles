node {
    stage('Preparation') {
        currentBuild.displayName = "Build_" + "${BUILD_TIMESTAMP}"
        git 'git@github.com:Javier-Caballero-Info/personal_page_nginx.git'
    }
    stage('Docker build'){
        sh '/usr/local/bin/docker build -t javiercaballeroinfo/personal_page_nginx:$Docker_Tag .'
    }
    stage('Docker push'){
        sh '/usr/local/bin/docker login -u $DOCKER_USER -p $DOCKER_PASSWORD'
        sh '/usr/local/bin/docker push javiercaballeroinfo/personal_page_nginx:$Docker_Tag'
    }
    stage('Update Deployer Manager'){
        httpRequest acceptType: 'APPLICATION_JSON', contentType: 'APPLICATION_JSON', httpMode: 'PUT', responseHandle: 'NONE', url: 'http://deployer.javiercaballero.info/api/v1/app_versions?app_id=5c342891a51e270010e31134', validResponseCodes: '202'
    }
}