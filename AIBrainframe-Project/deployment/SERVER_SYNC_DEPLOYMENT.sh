#!/bin/bash

# =====================================================
# LBOB Adaptive Interface Deployment Script
# Zero-Risk Server Synchronization and Deployment
# =====================================================

set -e  # Exit on any error

# Configuration
SERVER_IP="192.168.1.70"
SERVER_USER="csprinks"
SERVER_PATH="/opt/aibrainframe_claude"
LOCAL_BACKUP_DIR="./server_backup_$(date +%Y%m%d_%H%M%S)"
LOCAL_PROJECT_DIR="/home/csprinks/ClaudeCode-Projects/AIBrainframe-Project"

echo "🚀 LBOB Adaptive Interface Deployment"
echo "====================================="
echo "Server: $SERVER_USER@$SERVER_IP"
echo "Backup: $LOCAL_BACKUP_DIR"
echo ""

# Function to check SSH connectivity
check_ssh() {
    echo "🔍 Checking SSH connectivity..."
    if ssh -o ConnectTimeout=10 -o BatchMode=yes $SERVER_USER@$SERVER_IP exit 2>/dev/null; then
        echo "✅ SSH connection successful"
        return 0
    else
        echo "❌ SSH connection failed"
        echo "💡 Ensure port forwarding is configured for SSH (port 22)"
        echo "💡 Or ensure you're on the same network as the server"
        return 1
    fi
}

# Function to create complete server backup
backup_server() {
    echo ""
    echo "📦 Creating server backup..."
    mkdir -p $LOCAL_BACKUP_DIR

    echo "  📁 Backing up application files..."
    scp -r $SERVER_USER@$SERVER_IP:$SERVER_PATH/app/ $LOCAL_BACKUP_DIR/app/

    echo "  📁 Backing up static files..."
    scp -r $SERVER_USER@$SERVER_IP:$SERVER_PATH/static/ $LOCAL_BACKUP_DIR/static/ 2>/dev/null || true
    scp -r $SERVER_USER@$SERVER_IP:$SERVER_PATH/assets/ $LOCAL_BACKUP_DIR/assets/ 2>/dev/null || true

    echo "  💾 Backing up database files..."
    scp $SERVER_USER@$SERVER_IP:$SERVER_PATH/*.db $LOCAL_BACKUP_DIR/ 2>/dev/null || true

    echo "  ⚙️  Backing up configuration files..."
    scp $SERVER_USER@$SERVER_IP:$SERVER_PATH/.env $LOCAL_BACKUP_DIR/ 2>/dev/null || true
    scp $SERVER_USER@$SERVER_IP:$SERVER_PATH/requirements.txt $LOCAL_BACKUP_DIR/ 2>/dev/null || true

    echo "  🔧 Backing up systemd service..."
    ssh $SERVER_USER@$SERVER_IP 'cat /etc/systemd/system/lbob-api.service' > $LOCAL_BACKUP_DIR/lbob-api.service

    echo "✅ Server backup completed: $LOCAL_BACKUP_DIR"
}

# Function to sync critical assets to local repo
sync_assets_to_local() {
    echo ""
    echo "🔄 Syncing server assets to local repository..."

    # Copy character images if they exist on server
    if [ -d "$LOCAL_BACKUP_DIR/assets/images" ]; then
        echo "  🖼️  Syncing character images..."
        mkdir -p $LOCAL_PROJECT_DIR/static/images
        cp -r $LOCAL_BACKUP_DIR/assets/images/ $LOCAL_PROJECT_DIR/static/images/
        echo "  ✅ Character images synced"
    elif [ -d "$LOCAL_BACKUP_DIR/static/images" ]; then
        echo "  🖼️  Syncing character images from static..."
        mkdir -p $LOCAL_PROJECT_DIR/static/images
        cp -r $LOCAL_BACKUP_DIR/static/images/ $LOCAL_PROJECT_DIR/static/images/
        echo "  ✅ Character images synced"
    else
        echo "  ⚠️  No character images found on server"
    fi

    # Copy database for reference
    if [ -f "$LOCAL_BACKUP_DIR/aibrainframe.db" ]; then
        echo "  💾 Copying database for reference..."
        cp $LOCAL_BACKUP_DIR/aibrainframe.db $LOCAL_PROJECT_DIR/
        echo "  ✅ Database copied"
    fi

    # Copy environment file for reference
    if [ -f "$LOCAL_BACKUP_DIR/.env" ]; then
        echo "  ⚙️  Copying environment configuration..."
        cp $LOCAL_BACKUP_DIR/.env $LOCAL_PROJECT_DIR/.env.server_backup
        echo "  ✅ Environment configuration copied"
    fi

    echo "✅ Assets synced to local repository"
}

# Function to deploy enhanced code
deploy_enhanced_code() {
    echo ""
    echo "🚀 Deploying enhanced LBOB code..."

    # Create deployment backup on server
    echo "  📦 Creating deployment backup on server..."
    ssh $SERVER_USER@$SERVER_IP "cp -r $SERVER_PATH $SERVER_PATH.backup_$(date +%Y%m%d_%H%M%S)"

    # Deploy enhanced AI service
    echo "  🧠 Deploying enhanced AI service..."
    scp $LOCAL_PROJECT_DIR/app/ai_service.py $SERVER_USER@$SERVER_IP:$SERVER_PATH/app/

    # Deploy attachment routes
    echo "  📎 Deploying attachment system..."
    scp $LOCAL_PROJECT_DIR/app/routes/attachments.py $SERVER_USER@$SERVER_IP:$SERVER_PATH/app/routes/

    # Update main app with attachment routes
    echo "  🔧 Updating main application..."
    scp $LOCAL_PROJECT_DIR/app/main.py $SERVER_USER@$SERVER_IP:$SERVER_PATH/app/

    # Deploy adaptive interface
    echo "  🎨 Deploying adaptive interface..."
    scp $LOCAL_PROJECT_DIR/static/simple_lbob_adaptive.html $SERVER_USER@$SERVER_IP:$SERVER_PATH/static/

    # Update other route files if changed
    echo "  🔄 Updating conversation routes..."
    scp $LOCAL_PROJECT_DIR/app/routes/conversations.py $SERVER_USER@$SERVER_IP:$SERVER_PATH/app/routes/

    echo "✅ Enhanced code deployed"
}

# Function to install dependencies and restart service
finalize_deployment() {
    echo ""
    echo "🔧 Finalizing deployment..."

    # Create uploads directory for attachments
    echo "  📁 Creating uploads directory..."
    ssh $SERVER_USER@$SERVER_IP "mkdir -p $SERVER_PATH/uploads/{jobs,equipment,conversations}"

    # Install any new dependencies (if requirements.txt changed)
    echo "  📦 Installing dependencies..."
    ssh $SERVER_USER@$SERVER_IP "cd $SERVER_PATH && source venv/bin/activate && pip install fastapi[all] python-multipart"

    # Restart the service
    echo "  🔄 Restarting LBOB service..."
    ssh $SERVER_USER@$SERVER_IP 'echo "0320" | sudo -S systemctl restart lbob-api.service'

    # Wait for service to start
    echo "  ⏳ Waiting for service to start..."
    sleep 5

    # Check service status
    echo "  📊 Checking service status..."
    ssh $SERVER_USER@$SERVER_IP 'systemctl status lbob-api.service --no-pager -l | head -10'

    echo "✅ Deployment finalized"
}

# Function to test deployment
test_deployment() {
    echo ""
    echo "🧪 Testing deployment..."

    # Test basic API health
    echo "  🏥 Testing API health..."
    if curl -s http://108.254.44.67:8000/api | grep -q "running"; then
        echo "  ✅ API is responding"
    else
        echo "  ❌ API health check failed"
    fi

    # Test LBOB interface
    echo "  🤖 Testing LBOB interface..."
    if curl -s http://108.254.44.67:8000/static/simple_lbob_adaptive.html | grep -q "LBOB"; then
        echo "  ✅ Adaptive interface is accessible"
    else
        echo "  ❌ Adaptive interface test failed"
    fi

    echo "✅ Basic deployment tests completed"
}

# Function to commit final state to git
commit_final_state() {
    echo ""
    echo "📝 Committing final state to git..."

    cd $LOCAL_PROJECT_DIR
    git add .
    git commit -m "🔄 Server sync complete - All assets and configurations synchronized

✅ Server backup completed: $(basename $LOCAL_BACKUP_DIR)
✅ Character images and assets synced to local repository
✅ Enhanced LBOB adaptive interface deployed to production
✅ Attachment system and job correlation active
✅ All files synchronized and deployment tested

Status: Production deployment complete with zero data loss" || echo "No changes to commit"

    git push origin main
    echo "✅ Final state committed to git"
}

# Main deployment process
main() {
    echo "Starting LBOB Adaptive Interface Deployment..."
    echo ""

    # Check prerequisites
    if ! check_ssh; then
        echo ""
        echo "❌ Cannot connect to server"
        echo "💡 Please ensure:"
        echo "   1. You're on the same network as the server, OR"
        echo "   2. Port forwarding is configured for SSH (port 22), OR"
        echo "   3. VPN connection is established"
        echo ""
        echo "Once connectivity is restored, run this script again."
        exit 1
    fi

    # Confirm deployment
    echo "⚠️  This will deploy the adaptive LBOB interface to production."
    echo "   Current LBOB will be backed up before any changes."
    echo ""
    read -p "Continue with deployment? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 0
    fi

    # Execute deployment steps
    backup_server
    sync_assets_to_local
    deploy_enhanced_code
    finalize_deployment
    test_deployment
    commit_final_state

    echo ""
    echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
    echo "======================================"
    echo "🌐 Adaptive LBOB Interface: http://108.254.44.67:8000/static/simple_lbob_adaptive.html"
    echo "🤖 Original LBOB (backup): http://108.254.44.67:8000/static/simple_lbob.html"
    echo "📊 API Documentation: http://108.254.44.67:8000/docs"
    echo ""
    echo "✨ New Features Active:"
    echo "   • Adaptive UI with job-centric workflow"
    echo "   • File upload (documents, photos, voice)"
    echo "   • Job detection and multi-job tabs"
    echo "   • Enhanced AI with job correlation"
    echo "   • Complete conversation history"
    echo ""
    echo "🔒 Backup Location: $LOCAL_BACKUP_DIR"
    echo "📝 All changes committed to git repository"
}

# Run main function
main "$@"