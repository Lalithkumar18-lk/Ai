import streamlit as st
import pandas as pd
import datetime
import json
import random
import time
from typing import List, Dict, Optional
import plotly.graph_objects as go
import plotly.express as px

# Initialize session state
if 'cases' not in st.session_state:
    st.session_state.cases = []
if 'case_counter' not in st.session_state:
    st.session_state.case_counter = 1000
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        'cases_handled': 0,
        'avg_resolution_time': 0,
        'satisfaction_score': 0
    }

# Page configuration
st.set_page_config(
    page_title="AI Ethics Case Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .case-urgent { background-color: #fee; border-left: 5px solid #e74c3c; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .case-high { background-color: #fef9e7; border-left: 5px solid #f39c12; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .case-medium { background-color: #e8f4fc; border-left: 5px solid #3498db; padding: 10px; border-radius: 5px; margin: 5px 0; }
    .case-low { background-color: #eafaf1; border-left: 5px solid #27ae60; padding: 10px; border-radius: 5px; margin: 5px 0; }
    
    .status-open { color: #e74c3c; font-weight: bold; }
    .status-investigating { color: #f39c12; font-weight: bold; }
    .status-resolved { color: #27ae60; font-weight: bold; }
    .status-escalated { color: #8e44ad; font-weight: bold; }
    
    .chat-user { background-color: #e3f2fd; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%; float: right; clear: both; }
    .chat-ai { background-color: #f5f5f5; padding: 10px; border-radius: 10px; margin: 5px 0; max-width: 80%; float: left; clear: both; }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .real-time-alert {
        animation: blink 1s infinite;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
""", unsafe_allow_html=True)

# Case Data Models
class AICase:
    def __init__(self, case_id: str, title: str, description: str, category: str, 
                 priority: str, reported_by: str, platform: str = "Unknown"):
        self.id = case_id
        self.title = title
        self.description = description
        self.category = category
        self.priority = priority  # "urgent", "high", "medium", "low"
        self.status = "open"
        self.reported_by = reported_by
        self.platform = platform
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.resolution = ""
        self.advocacy_actions = []
        self.chat_history = []
        self.assigned_to = ""
        self.severity_score = random.randint(1, 100)
        self.affected_users = random.randint(100, 10000)
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "status": self.status,
            "reported_by": self.reported_by,
            "platform": self.platform,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "severity_score": self.severity_score,
            "affected_users": self.affected_users,
            "resolution": self.resolution,
            "advocacy_actions": self.advocacy_actions,
            "assigned_to": self.assigned_to
        }

# Predefined cases
PREDEFINED_CASES = [
    {
        "title": "Algorithmic Bias in Hiring Platform",
        "description": "AI recruiting tool showing significant gender bias, favoring male candidates over equally qualified female candidates in tech roles.",
        "category": "Bias & Discrimination",
        "priority": "urgent",
        "platform": "TechHire AI",
        "affected_demo": "Women in tech"
    },
    {
        "title": "Healthcare AI Misdiagnosis",
        "description": "Medical diagnostic AI incorrectly diagnosing rare diseases, leading to delayed treatment for 200+ patients.",
        "category": "Healthcare Safety",
        "priority": "urgent",
        "platform": "MedScan AI",
        "affected_demo": "Patients with rare diseases"
    },
    {
        "title": "Facial Recognition False Positives",
        "description": "Law enforcement facial recognition system misidentifying individuals, disproportionately affecting minority communities.",
        "category": "Privacy & Surveillance",
        "priority": "high",
        "platform": "SafeCity AI",
        "affected_demo": "Minority communities"
    },
    {
        "title": "Social Media Recommendation Harm",
        "description": "AI recommendation algorithm promoting harmful content to teenagers, linked to mental health issues.",
        "category": "Content Moderation",
        "priority": "high",
        "platform": "SocialFlow",
        "affected_demo": "Teenagers"
    },
    {
        "title": "Autonomous Vehicle Ethics Dilemma",
        "description": "Self-driving car algorithm showing inconsistent decision-making in accident scenarios, raising ethical concerns.",
        "category": "Autonomous Systems",
        "priority": "medium",
        "platform": "AutoDrive Inc",
        "affected_demo": "General public"
    },
    {
        "title": "Financial AI Loan Discrimination",
        "description": "AI loan approval system systematically denying applications from certain zip codes, perpetuating historical redlining.",
        "category": "Financial Equity",
        "priority": "urgent",
        "platform": "FinTech Solutions",
        "affected_demo": "Low-income neighborhoods"
    }
]

# Advocacy Action Templates
ADVOCACY_TEMPLATES = {
    "Legal": [
        "File regulatory complaint with relevant authority",
        "Initiate class action lawsuit preparations",
        "Request algorithmic transparency under GDPR/CCPA",
        "Submit Freedom of Information Act request"
    ],
    "Media": [
        "Prepare press release for media outlets",
        "Contact investigative journalists",
        "Draft op-ed for major newspapers",
        "Create social media awareness campaign"
    ],
    "Technical": [
        "Request independent algorithmic audit",
        "Demand source code review",
        "Propose third-party validation",
        "Request bias mitigation implementation"
    ],
    "Community": [
        "Organize community forum with affected individuals",
        "Create online petition",
        "Coordinate with advocacy groups",
        "Host public awareness webinar"
    ],
    "Corporate": [
        "Schedule meeting with company executives",
        "Propose ethical AI review board",
        "Demand public transparency report",
        "Request immediate system suspension"
    ]
}

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092683.png", width=80)
    st.title("🤖 AI Ethics Case Management")
    
    st.markdown("---")
    
    # Real-time alert
    if random.random() > 0.7 and st.session_state.cases:
        st.markdown('<div class="real-time-alert">🚨 New case update available!</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.subheader("📊 Live Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Cases", len([c for c in st.session_state.cases if c.status != "resolved"]))
    with col2:
        st.metric("Urgent", len([c for c in st.session_state.cases if c.priority == "urgent" and c.status != "resolved"]))
    
    st.markdown("---")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    if st.button("🆕 Generate Test Case", use_container_width=True):
        case_data = random.choice(PREDEFINED_CASES)
        case_id = f"CASE-{st.session_state.case_counter}"
        new_case = AICase(
            case_id=case_id,
            title=case_data["title"],
            description=case_data["description"],
            category=case_data["category"],
            priority=case_data["priority"],
            reported_by="System Generated",
            platform=case_data["platform"]
        )
        st.session_state.cases.append(new_case)
        st.session_state.case_counter += 1
        st.session_state.analytics['cases_handled'] += 1
        st.rerun()
    
    if st.button("📊 Update Analytics", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    # Team Assignment
    st.subheader("👥 Team")
    team_members = ["Alex Chen", "Maria Garcia", "David Kim", "Sarah Johnson", "James Wilson"]
    selected_assignee = st.selectbox("Assign to:", ["Unassigned"] + team_members)

# Main content
st.markdown('<h1 class="main-header">⚖️ Real-Time AI Ethics Case Management System</h1>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Case Dashboard", 
    "🔍 Case Details", 
    "💬 Live Resolution", 
    "📈 Analytics", 
    "📢 Advocacy Center"
])

with tab1:  # Case Dashboard
    st.subheader("🔄 Real-Time Case Monitoring")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_priority = st.selectbox("Priority", ["All", "urgent", "high", "medium", "low"])
    with col2:
        filter_status = st.selectbox("Status", ["All", "open", "investigating", "escalated", "resolved"])
    with col3:
        filter_category = st.selectbox("Category", ["All", "Bias & Discrimination", "Healthcare Safety", 
                                                  "Privacy & Surveillance", "Content Moderation", 
                                                  "Autonomous Systems", "Financial Equity"])
    with col4:
        filter_platform = st.text_input("Platform")
    
    # Display cases
    st.subheader("📋 Active Cases")
    
    filtered_cases = st.session_state.cases
    
    if filter_priority != "All":
        filtered_cases = [c for c in filtered_cases if c.priority == filter_priority]
    if filter_status != "All":
        filtered_cases = [c for c in filtered_cases if c.status == filter_status]
    if filter_category != "All":
        filtered_cases = [c for c in filtered_cases if c.category == filter_category]
    if filter_platform:
        filtered_cases = [c for c in filtered_cases if filter_platform.lower() in c.platform.lower()]
    
    for case in filtered_cases:
        priority_class = f"case-{case.priority}"
        
        with st.container():
            st.markdown(f"""
            <div class="{priority_class}">
                <h4>{case.title} <span class="status-{case.status}">[{case.status.upper()}]</span></h4>
                <p><strong>Category:</strong> {case.category} | <strong>Platform:</strong> {case.platform}</p>
                <p><strong>Reported:</strong> {case.created_at.strftime('%Y-%m-%d %H:%M')} | 
                <strong>Affected Users:</strong> {case.affected_users:,}</p>
                <p><strong>Severity Score:</strong> {case.severity_score}/100</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1,1,2])
            with col1:
                if st.button(f"View Details", key=f"view_{case.id}"):
                    st.session_state.selected_case = case.id
                    st.rerun()
            with col2:
                if case.status != "resolved":
                    new_status = st.selectbox("Update Status", 
                                             ["open", "investigating", "escalated", "resolved"],
                                             key=f"status_{case.id}",
                                             index=["open", "investigating", "escalated", "resolved"].index(case.status))
                    if new_status != case.status:
                        case.status = new_status
                        case.updated_at = datetime.datetime.now()
                        st.rerun()
            with col3:
                if case.assigned_to:
                    st.info(f"Assigned to: {case.assigned_to}")
                else:
                    if st.button("Assign to me", key=f"assign_{case.id}"):
                        case.assigned_to = selected_assignee if selected_assignee != "Unassigned" else "You"
                        st.rerun()
    
    if not filtered_cases:
        st.info("No cases match the current filters. Try generating a test case!")

with tab2:  # Case Details
    st.subheader("🔍 Case Investigation Panel")
    
    if 'selected_case' in st.session_state and st.session_state.selected_case:
        case_id = st.session_state.selected_case
        case = next((c for c in st.session_state.cases if c.id == case_id), None)
        
        if case:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### {case.title}")
                st.markdown(f"**Case ID:** {case.id}")
                st.markdown(f"**Platform:** {case.platform}")
                st.markdown(f"**Category:** {case.category}")
                st.markdown(f"**Priority:** {case.priority}")
                st.markdown(f"**Status:** {case.status}")
                st.markdown(f"**Reported By:** {case.reported_by}")
                st.markdown(f"**Created:** {case.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Last Updated:** {case.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                st.markdown("---")
                st.subheader("📝 Case Description")
                st.write(case.description)
                
                st.markdown("---")
                st.subheader("📊 Impact Assessment")
                
                col_imp1, col_imp2, col_imp3 = st.columns(3)
                with col_imp1:
                    st.metric("Affected Users", f"{case.affected_users:,}")
                with col_imp2:
                    st.metric("Severity Score", f"{case.severity_score}/100")
                with col_imp3:
                    days_open = (datetime.datetime.now() - case.created_at).days
                    st.metric("Days Open", days_open)
                
                # Timeline visualization
                st.markdown("### 📅 Case Timeline")
                timeline_data = pd.DataFrame({
                    'Event': ['Case Opened', 'Initial Review', 'Investigation', 'Current'],
                    'Date': [
                        case.created_at,
                        case.created_at + datetime.timedelta(hours=2),
                        case.created_at + datetime.timedelta(days=1),
                        datetime.datetime.now()
                    ]
                })
                timeline_data['Days Since Start'] = (timeline_data['Date'] - case.created_at).dt.days
                st.line_chart(timeline_data.set_index('Event')['Days Since Start'])
            
            with col2:
                st.subheader("🛠️ Quick Actions")
                
                # Status update
                new_status = st.selectbox("Update Case Status", 
                                         ["open", "investigating", "escalated", "resolved"],
                                         index=["open", "investigating", "escalated", "resolved"].index(case.status))
                if new_status != case.status:
                    case.status = new_status
                    case.updated_at = datetime.datetime.now()
                    st.success(f"Status updated to {new_status}")
                
                # Assignment
                assign_to = st.selectbox("Assign Case", 
                                        ["Unassigned", "Alex Chen", "Maria Garcia", "David Kim", "Sarah Johnson", "James Wilson"],
                                        index=0 if not case.assigned_to else ["Unassigned", "Alex Chen", "Maria Garcia", "David Kim", "Sarah Johnson", "James Wilson"].index(case.assigned_to))
                if assign_to != case.assigned_to:
                    case.assigned_to = assign_to
                    st.success(f"Assigned to {assign_to}")
                
                st.markdown("---")
                
                # Resolution input
                st.subheader("✅ Resolution")
                resolution_text = st.text_area("Enter resolution details:", case.resolution, height=150)
                if resolution_text != case.resolution:
                    case.resolution = resolution_text
                    if resolution_text and case.status != "resolved":
                        case.status = "resolved"
                
                if st.button("Save Resolution"):
                    st.success("Resolution saved!")
                
                st.markdown("---")
                
                # Quick advocacy actions
                st.subheader("⚡ Quick Advocacy")
                action_type = st.selectbox("Action Type", list(ADVOCACY_TEMPLATES.keys()))
                if action_type:
                    selected_action = st.selectbox("Select Action", ADVOCACY_TEMPLATES[action_type])
                    if st.button(f"Add {action_type} Action"):
                        case.advocacy_actions.append({
                            "type": action_type,
                            "action": selected_action,
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "pending"
                        })
                        st.success(f"Added {action_type} action: {selected_action}")
                
                # View all advocacy actions
                if case.advocacy_actions:
                    st.markdown("#### 📋 Advocacy Actions")
                    for i, action in enumerate(case.advocacy_actions):
                        st.write(f"{i+1}. **{action['type']}**: {action['action']} ({action['date']})")
        else:
            st.warning("Case not found. Please select a valid case.")
    else:
        st.info("Select a case from the Dashboard to view details.")

with tab3:  # Live Resolution
    st.subheader("💬 Live Case Resolution Chat")
    
    if 'selected_case' in st.session_state and st.session_state.selected_case:
        case_id = st.session_state.selected_case
        case = next((c for c in st.session_state.cases if c.id == case_id), None)
        
        if case:
            st.markdown(f"### Chat for Case: {case.title}")
            
            # Chat interface
            chat_container = st.container()
            
            with chat_container:
                # Display chat history
                for msg in case.chat_history:
                    if msg["sender"] == "user":
                        st.markdown(f'<div class="chat-user"><strong>You:</strong> {msg["message"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-ai"><strong>AI Advisor:</strong> {msg["message"]}</div>', unsafe_allow_html=True)
            
            # Chat input
            st.markdown("---")
            col_chat1, col_chat2 = st.columns([4, 1])
            
            with col_chat1:
                user_message = st.text_input("Type your message:", key="chat_input")
            
            with col_chat2:
                if st.button("Send", use_container_width=True):
                    if user_message:
                        # Add user message
                        case.chat_history.append({
                            "sender": "user",
                            "message": user_message,
                            "time": datetime.datetime.now().strftime("%H:%M")
                        })
                        
                        # Generate AI response (simulated)
                        ai_responses = [
                            "Based on similar cases, I recommend documenting all evidence systematically.",
                            "Consider contacting the platform's ethics committee directly.",
                            "Have you reviewed the platform's algorithmic accountability report?",
                            "This might require escalating to regulatory authorities.",
                            "I suggest conducting an independent impact assessment first.",
                            "Let's identify all stakeholders affected by this issue."
                        ]
                        
                        ai_response = random.choice(ai_responses)
                        case.chat_history.append({
                            "sender": "ai",
                            "message": ai_response,
                            "time": datetime.datetime.now().strftime("%H:%M")
                        })
                        
                        st.rerun()
            
            # Quick response buttons
            st.markdown("#### 💡 Quick Suggestions")
            quick_responses = [
                "What's the first step?",
                "Who should we contact?",
                "Documentation needed?",
                "Legal implications?",
                "Media strategy?"
            ]
            
            cols = st.columns(len(quick_responses))
            for idx, resp in enumerate(quick_responses):
                with cols[idx]:
                    if st.button(resp, key=f"quick_{idx}"):
                        case.chat_history.append({
                            "sender": "user",
                            "message": resp,
                            "time": datetime.datetime.now().strftime("%H:%M")
                        })
                        
                        # AI response logic here
                        st.rerun()
            
            # Resolution progress
            st.markdown("---")
            st.subheader("📊 Resolution Progress")
            
            if not case.resolution:
                resolution_steps = ["Investigation", "Evidence Collection", "Stakeholder Engagement", 
                                   "Solution Design", "Implementation", "Verification"]
                
                current_step = min(len(case.chat_history) // 3, len(resolution_steps) - 1)
                
                progress_df = pd.DataFrame({
                    'Step': resolution_steps,
                    'Status': ['completed' if i < current_step else 'current' if i == current_step else 'pending' 
                              for i in range(len(resolution_steps))]
                })
                
                # Create progress bar
                progress = (current_step / (len(resolution_steps) - 1)) * 100
                st.progress(int(progress))
                st.write(f"Progress: {current_step + 1}/{len(resolution_steps)} steps completed")
                
                # Display steps
                for i, step in enumerate(resolution_steps):
                    status_icon = "✅" if i < current_step else "🔄" if i == current_step else "⏳"
                    st.write(f"{status_icon} {step}")
        else:
            st.warning("Please select a case first.")
    else:
        st.info("Select a case from the Dashboard to start live resolution.")

with tab4:  # Analytics
    st.subheader("📈 Real-Time Analytics Dashboard")
    
    if st.session_state.cases:
        # Convert cases to dataframe
        cases_df = pd.DataFrame([c.to_dict() for c in st.session_state.cases])
        
        col_a1, col_a2, col_a3, col_a4 = st.columns(4)
        
        with col_a1:
            active_cases = len([c for c in st.session_state.cases if c.status != "resolved"])
            st.metric("Active Cases", active_cases)
        
        with col_a2:
            urgent_cases = len([c for c in st.session_state.cases if c.priority == "urgent" and c.status != "resolved"])
            st.metric("Urgent Cases", urgent_cases)
        
        with col_a3:
            avg_severity = sum(c.severity_score for c in st.session_state.cases) / len(st.session_state.cases)
            st.metric("Avg Severity", f"{avg_severity:.1f}/100")
        
        with col_a4:
            resolution_rate = len([c for c in st.session_state.cases if c.status == "resolved"]) / len(st.session_state.cases) * 100
            st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📊 Cases by Category")
            category_counts = cases_df['category'].value_counts()
            fig1 = px.pie(values=category_counts.values, names=category_counts.index)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_chart2:
            st.subheader("📈 Cases by Priority")
            priority_counts = cases_df['priority'].value_counts()
            fig2 = px.bar(x=priority_counts.index, y=priority_counts.values, 
                         color=priority_counts.index,
                         color_discrete_map={'urgent': 'red', 'high': 'orange', 
                                           'medium': 'blue', 'low': 'green'})
            st.plotly_chart(fig2, use_container_width=True)
        
        # Time-based analysis
        st.subheader("⏱️ Resolution Time Analysis")
        
        if len(cases_df) > 1:
            # Convert date strings to datetime
            cases_df['created_at'] = pd.to_datetime(cases_df['created_at'])
            cases_df['updated_at'] = pd.to_datetime(cases_df['updated_at'])
            
            # Calculate resolution time
            resolved_cases = cases_df[cases_df['status'] == 'resolved'].copy()
            if not resolved_cases.empty:
                resolved_cases['resolution_hours'] = (resolved_cases['updated_at'] - resolved_cases['created_at']).dt.total_seconds() / 3600
                
                fig3 = px.histogram(resolved_cases, x='resolution_hours', 
                                   nbins=10, title='Resolution Time Distribution')
                st.plotly_chart(fig3, use_container_width=True)
        
        # Platform analysis
        st.subheader("🖥️ Cases by Platform")
        platform_counts = cases_df['platform'].value_counts().head(10)
        fig4 = px.bar(y=platform_counts.index, x=platform_counts.values, 
                     orientation='h', title='Top Platforms with Issues')
        st.plotly_chart(fig4, use_container_width=True)
        
        # Real-time updates
        st.markdown("---")
        st.subheader("🔄 Live Updates")
        
        # Simulate real-time updates
        if st.button("Simulate New Case Stream"):
            with st.spinner("Streaming live case data..."):
                for i in range(3):
                    time.sleep(1)
                    case_data = random.choice(PREDEFINED_CASES)
                    case_id = f"LIVE-{st.session_state.case_counter}"
                    new_case = AICase(
                        case_id=case_id,
                        title=f"[LIVE] {case_data['title']}",
                        description=case_data["description"],
                        category=case_data["category"],
                        priority=case_data["priority"],
                        reported_by="Live Stream",
                        platform=case_data["platform"]
                    )
                    st.session_state.cases.append(new_case)
                    st.session_state.case_counter += 1
                    st.success(f"Live case added: {new_case.title}")
                
                st.rerun()
    else:
        st.info("No cases yet. Generate some test cases to see analytics!")

with tab5:  # Advocacy Center
    st.subheader("📢 AI Advocacy Action Center")
    
    col_adv1, col_adv2 = st.columns([2, 1])
    
    with col_adv1:
        st.markdown("### 🎯 Strategic Advocacy Planning")
        
        # Current issues heatmap
        st.markdown("#### 🔥 Current AI Ethics Hotspots")
        
        issues_data = pd.DataFrame({
            'Issue': ['Algorithmic Bias', 'Privacy Violations', 'Misinformation', 
                     'Autonomous Weapons', 'Job Displacement', 'Surveillance'],
            'Severity': [95, 88, 76, 92, 68, 85],
            'Media Attention': [85, 70, 95, 60, 75, 65]
        })
        
        fig = px.scatter(issues_data, x='Media Attention', y='Severity', 
                        size='Severity', color='Issue', hover_name='Issue',
                        title='AI Ethics Issues Heatmap')
        st.plotly_chart(fig, use_container_width=True)
        
        # Advocacy campaign builder
        st.markdown("### 🛠️ Build Advocacy Campaign")
        
        campaign_name = st.text_input("Campaign Name", "Stop Algorithmic Bias in Hiring")
        
        col_camp1, col_camp2 = st.columns(2)
        with col_camp1:
            target_platform = st.selectbox("Target Platform/Company", 
                                          ["All Tech Companies", "FAANG", "Healthcare AI", 
                                           "Financial Services", "Government", "Social Media"])
        
        with col_camp2:
            campaign_type = st.selectbox("Campaign Type", 
                                        ["Awareness", "Policy Change", "Legal Action", 
                                         "Technical Reform", "Community Organizing"])
        
        st.markdown("#### 📝 Campaign Actions")
        
        selected_actions = []
        for category, actions in ADVOCACY_TEMPLATES.items():
            with st.expander(f"📋 {category} Actions"):
                for action in actions:
                    if st.checkbox(action, key=f"action_{action[:20]}"):
                        selected_actions.append(f"{category}: {action}")
        
        if selected_actions:
            st.markdown("#### ✅ Selected Actions")
            for action in selected_actions:
                st.write(f"• {action}")
        
        if st.button("🚀 Launch Campaign"):
            st.success(f"Campaign '{campaign_name}' launched with {len(selected_actions)} actions!")
            # Here you would save the campaign to a database
    
    with col_adv2:
        st.markdown("### 📊 Advocacy Metrics")
        
        # Success metrics
        st.metric("Campaigns Active", "12")
        st.metric("Policy Changes", "3")
        st.metric("Media Mentions", "245")
        st.metric("Community Support", "15,234")
        
        st.markdown("---")
        
        st.markdown("### 📢 Recent Wins")
        
        wins = [
            "Tech company agrees to independent AI audit",
            "New legislation proposed for AI transparency",
            "Major platform removes biased algorithm",
            "Class action lawsuit settlement reached"
        ]
        
        for win in wins:
            st.success(f"✅ {win}")
        
        st.markdown("---")
        
        st.markdown("### 🔄 Live Advocacy Feed")
        
        # Simulated live feed
        feed_items = [
            "Breaking: New AI ethics guidelines released by EU",
            "Protest organized outside TechCorp HQ",
            "Op-ed published in NY Times about AI bias",
            "Petition reaches 50,000 signatures",
            "Congressional hearing on AI scheduled"
        ]
        
        for item in feed_items:
            st.info(f"📢 {item}")
            time.sleep(0.1)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
    <p>⚖️ <strong>AI Ethics Case Management System v2.0</strong> | Real-time monitoring and advocacy platform</p>
    <p>For reporting AI ethics issues: ethics@ai-advocate.org | Hotline: 1-800-AI-ETHICS</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Auto-refresh for real-time feel
if st.checkbox("🔄 Enable auto-refresh (every 30 seconds)"):
    time.sleep(30)
    st.rerun()
