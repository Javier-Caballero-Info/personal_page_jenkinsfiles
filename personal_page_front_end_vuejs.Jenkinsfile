node {
    stage('Preparation') {
        currentBuild.displayName = "Build_" + "${BUILD_TIMESTAMP}"
        git 'git@github.com:Javier-Caballero-Info/personal_page_front_end_vuejs.git'
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
    stage('Firebase Deploy'){
        nodejs('Node10.15.0') {
            sh 'firebase deploy'
        }
    }
}