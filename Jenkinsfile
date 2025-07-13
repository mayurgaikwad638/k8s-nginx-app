// Jenkinsfile
pipeline {
    agent any // The pipeline will run on your Jenkins host machine

    environment {
        // Your Docker Hub username (use your actual Docker ID, e.g., mayurgaikwad638)
        DOCKER_HUB_USERNAME = 'kubemayurr' // <-- CONFIRM THIS IS YOUR CORRECT DOCKER HUB USERNAME

        // Define the base image names for Docker Hub.
        // We will append the Jenkins BUILD_NUMBER for unique versions.
        FRONTEND_IMAGE_BASE = "${DOCKER_HUB_USERNAME}/app-frontend" // Use your desired frontend repo name
        BACKEND_IMAGE_BASE = "${DOCKER_HUB_USERNAME}/app-backend"   // Use your desired backend repo name

        // Full image names with the dynamic tag for the current build
        FRONTEND_IMAGE_FULL = "${FRONTEND_IMAGE_BASE}:${env.BUILD_NUMBER}"
        BACKEND_IMAGE_FULL = "${BACKEND_IMAGE_BASE}:${env.BUILD_NUMBER}"

        // Paths to your application code and Kubernetes manifests, relative to the repository root
        FRONTEND_APP_PATH = "./frontend"
        BACKEND_APP_PATH = "./backend"
        KUBERNETES_MANIFESTS_PATH = "./k8s-files" // Path to your k8s manifest files
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Code checked out from GitHub repository 'k8s-nginx-app'."
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                script {
                    echo "Building Frontend Docker image: ${FRONTEND_IMAGE_FULL}"
                    // Builds the image using the Dockerfile inside the 'frontend' directory.
                    sh "docker build -t ${FRONTEND_IMAGE_FULL} ${FRONTEND_APP_PATH}"
                }
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                script {
                    echo "Building Backend Docker image: ${BACKEND_IMAGE_FULL}"
                    // Builds the image using the Dockerfile inside the 'backend' directory.
                    sh "docker build -t ${BACKEND_IMAGE_FULL} ${BACKEND_APP_PATH}"
                }
            }
        }

        stage('Push Docker Images to Docker Hub') {
            steps {
                // Uses the 'docker-hub-credentials' ID configured in Jenkins UI
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    script {
                        echo "Logging into Docker Hub..."
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'

                        echo "Pushing Frontend image: ${FRONTEND_IMAGE_FULL}"
                        sh "docker push ${FRONTEND_IMAGE_FULL}"

                        echo "Pushing Backend image: ${BACKEND_IMAGE_FULL}"
                        sh "docker push ${BACKEND_IMAGE_FULL}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Deploying to Kubernetes using kubectl from ${KUBERNETES_MANIFESTS_PATH}..."

                    // Apply Backend Kubernetes manifests (if necessary, for initial deploy or manifest changes)
                    // CONFIRM THESE FILENAMES MATCH YOUR ACTUAL FILES IN k8s-files
                    echo "Applying Backend Kubernetes manifest: ${KUBERNETES_MANIFESTS_PATH}/deployment.yml" // Assuming this name
                    sh "kubectl apply -f ${KUBERNETES_MANIFESTS_PATH}/deployment.yml"
                    echo "Applying Backend Kubernetes service: ${KUBERNETES_MANIFESTS_PATH}/service.yml" // Assuming this name
                    sh "kubectl apply -f ${KUBERNETES_MANIFESTS_PATH}/service.yml"


                    // Apply Frontend Kubernetes manifests (if necessary, for initial deploy or manifest changes)
                    // CONFIRM THESE FILENAMES MATCH YOUR ACTUAL FILES IN k8s-files
                    echo "Applying Frontend Kubernetes manifest: ${KUBERNETES_MANIFESTS_PATH}/frontend-deploy.yml" // Assuming this name
                    sh "kubectl apply -f ${KUBERNETES_MANIFESTS_PATH}/frontend-deploy.yml"
                    echo "Applying Frontend Kubernetes service: ${KUBERNETES_MANIFESTS_PATH}/frontend-svc.yml" // Assuming this name
                    sh "kubectl apply -f ${KUBERNETES_MANIFESTS_PATH}/frontend-svc.yml"


                    // Update Backend deployment with the new image tag
                    // 'backend-deploy' is the Deployment name (from your previous input)
                    // 'app-backend' is the container name (from your latest input)
                    echo "Setting image for Deployment 'backend-deploy', container 'app-backend' to ${BACKEND_IMAGE_FULL}"
                    sh "kubectl set image deployment/backend-deploy app-backend=${BACKEND_IMAGE_FULL}"

                    // Update Frontend deployment with the new image tag
                    // 'frontend-deploy' is the Deployment name (from your previous input)
                    // 'app-frontend' is the container name (from your latest input)
                    echo "Setting image for Deployment 'frontend-deploy', container 'app-frontend' to ${FRONTEND_IMAGE_FULL}"
                    sh "kubectl set image deployment/frontend-deploy app-frontend=${FRONTEND_IMAGE_FULL}"

                    echo "Kubernetes deployments updated."
                }
            }
        }

        stage('Verify Deployment (Optional)') {
            steps {
                script {
                    echo "Verifying Kubernetes deployment status..."
                    // Check specific deployments by name
                    sh 'kubectl get deployment backend-deploy'
                    sh 'kubectl get deployment frontend-deploy'
                    // Wait for rollouts to complete for each specific deployment
                    sh 'kubectl rollout status deployment/backend-deploy'
                    sh 'kubectl rollout status deployment/frontend-deploy'
                    // Check services by the confirmed service names
                    sh 'kubectl get svc backend-service' // Checking with your provided service name
                    sh 'kubectl get svc frontend-svc'    // Checking with your provided service name
                }
            }
        }
    }

    post {
        always {
            cleanWs() // Cleans up the Jenkins workspace directory after each pipeline run
        }
        success {
            echo 'Deployment Pipeline completed successfully! 🎉'
        }
        failure {
            echo 'Deployment Pipeline failed! ❌ Check console output for errors.'
        }
    }
}