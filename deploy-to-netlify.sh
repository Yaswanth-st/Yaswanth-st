#!/bin/bash

# 🚀 Smart Timetable System - Netlify Deployment Script
# Developed by TEAM SPIDERMERN

echo "🎓 Smart Timetable System - Netlify Deployment"
echo "==============================================="
echo "Developed by TEAM SPIDERMERN"
echo "SANJAY B • YASWANTH ST • ABISHECK AM"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "netlify-frontend" ]; then
    echo -e "${RED}❌ Error: netlify-frontend directory not found!${NC}"
    echo "Please run this script from the timetable_system directory."
    exit 1
fi

echo -e "${BLUE}📁 Found netlify-frontend directory${NC}"

# Function to create zip for manual upload
create_zip() {
    echo -e "${YELLOW}📦 Creating deployment package...${NC}"
    cd netlify-frontend
    
    # Remove any existing zip
    rm -f smart-timetable-frontend.zip
    
    # Create zip with all files
    zip -r smart-timetable-frontend.zip . -x "*.git*" "*.DS_Store*" "node_modules/*"
    
    echo -e "${GREEN}✅ Created smart-timetable-frontend.zip${NC}"
    echo -e "${BLUE}📤 Upload this file to Netlify for manual deployment${NC}"
    cd ..
}

# Function to deploy via Netlify CLI
deploy_cli() {
    echo -e "${YELLOW}🚀 Deploying via Netlify CLI...${NC}"
    
    # Check if Netlify CLI is installed
    if ! command -v netlify &> /dev/null; then
        echo -e "${RED}❌ Netlify CLI not found!${NC}"
        echo "Install it with: npm install -g netlify-cli"
        return 1
    fi
    
    cd netlify-frontend
    
    # Deploy to production
    echo -e "${BLUE}🚀 Deploying to production...${NC}"
    netlify deploy --prod --dir .
    
    echo -e "${GREEN}✅ Deployment complete!${NC}"
    cd ..
}

# Function to initialize git repository
init_git() {
    echo -e "${YELLOW}🔧 Initializing Git repository...${NC}"
    
    # Initialize git if not already done
    if [ ! -d ".git" ]; then
        git init
        echo -e "${GREEN}✅ Git repository initialized${NC}"
    else
        echo -e "${BLUE}📁 Git repository already exists${NC}"
    fi
    
    # Add netlify-frontend files
    git add netlify-frontend/
    git add deploy-to-netlify.sh
    
    # Commit changes
    git commit -m "Add Netlify frontend for Smart Timetable System by TEAM SPIDERMERN" 2>/dev/null || echo -e "${BLUE}📝 No new changes to commit${NC}"
}

# Function to show deployment instructions
show_instructions() {
    echo ""
    echo -e "${GREEN}🎉 Netlify Frontend Ready for Deployment!${NC}"
    echo ""
    echo -e "${BLUE}📋 Deployment Options:${NC}"
    echo ""
    echo "1. 📤 Manual Upload (Easiest)"
    echo "   - Go to https://netlify.com"
    echo "   - Drag and drop: netlify-frontend/smart-timetable-frontend.zip"
    echo "   - Your site will be live instantly!"
    echo ""
    echo "2. 🔗 Git Integration (Recommended)"
    echo "   - Push this repository to GitHub/GitLab"
    echo "   - Connect repository to Netlify"
    echo "   - Set build directory to 'netlify-frontend'"
    echo "   - Enable automatic deployments"
    echo ""
    echo "3. 💻 Netlify CLI (Advanced)"
    echo "   - Install: npm install -g netlify-cli"
    echo "   - Run: ./deploy-to-netlify.sh cli"
    echo ""
    echo -e "${YELLOW}⚙️ Next Steps:${NC}"
    echo "1. Deploy your Django backend (Heroku/Railway/Render)"
    echo "2. Update API URLs in netlify-frontend/netlify.toml"
    echo "3. Update API URLs in netlify-frontend/_redirects"
    echo "4. Update API URLs in netlify-frontend/js/main.js"
    echo ""
    echo -e "${GREEN}🏆 TEAM SPIDERMERN - Smart Timetable System${NC}"
}

# Main deployment logic
case "${1:-manual}" in
    "manual")
        echo -e "${BLUE}🎯 Preparing for manual deployment...${NC}"
        init_git
        create_zip
        show_instructions
        ;;
    "cli")
        echo -e "${BLUE}🎯 Using Netlify CLI deployment...${NC}"
        init_git
        deploy_cli
        show_instructions
        ;;
    "git")
        echo -e "${BLUE}🎯 Preparing for Git-based deployment...${NC}"
        init_git
        echo -e "${GREEN}✅ Repository ready for Git-based deployment${NC}"
        show_instructions
        ;;
    *)
        echo -e "${RED}❌ Invalid option: $1${NC}"
        echo "Usage: ./deploy-to-netlify.sh [manual|cli|git]"
        echo "  manual: Create zip for manual upload (default)"
        echo "  cli:    Deploy via Netlify CLI"
        echo "  git:    Prepare for Git-based deployment"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🚀 Ready to deploy your Smart Timetable System to Netlify!${NC}"