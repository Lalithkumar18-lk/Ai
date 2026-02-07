import streamlit as st
import pandas as pd
import datetime
import random
import time
import json
from typing import List, Dict, Optional

# Initialize session state
if 'advocacy_cases' not in st.session_state:
    st.session_state.advocacy_cases = []
if 'human_rights_violations' not in st.session_state:
    st.session_state.human_rights_violations = []
if 'impact_metrics' not in st.session_state:
    st.session_state.impact_metrics = {
        'people_protected': 0,
        'policies_influenced': 0,
        'awareness_campaigns': 0,
        'legal_interventions': 0
    }

# Page configuration
st.set_page_config(
    page_title="Human AI Advocate",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for human-centered design
st.markdown("""
<style>
    /* Human-centered theme colors */
    :root {
        --human-blue: #1a73e8;
        --human-green: #0d9d58;
        --human-red: #ea4335;
        --human-yellow: #fbbc04;
        --human-purple: #673ab7;
    }
    
    .human-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .rights-violation {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .success-story {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .advocacy-action {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .human-metric {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 4px solid var(--human-blue);
    }
    
    .urgent-alert {
        animation: pulse 2s infinite;
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .chat-human {
        background-color: #e3f2fd;
        padding: 12px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0;
        max-width: 70%;
        margin-left: auto;
    }
    
    .chat-ai {
        background-color: #f5f5f5;
        padding: 12px;
        border-radius: 15px 15px 15px 0;
        margin: 8px 0;
        max-width: 70%;
    }
    
    .impact-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        margin: 2px;
    }
    
    .impact-high { background-color: #ffebee; color: #c62828; }
    .impact-medium { background-color: #fff3e0; color: #ef6c00; }
    .impact-low { background-color: #e8f5e9; color: #2e7d32; }
    
    .stButton > button {
        background-color: var(--human-blue);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #0d47a1;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Data Models
class HumanAdvocacyCase:
    def __init__(self, case_id: str, title: str, description: str, 
                 human_right_affected: str, ai_system: str, severity: str):
        self.id = case_id
        self.title = title
        self.description = description
        self.human_right_affected = human_right_affected
        self.ai_system = ai_system
        self.severity = severity  # "critical", "high", "medium", "low"
        self.status = "reported"
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
        self.people_affected = random.randint(100, 100000)
        self.advocacy_actions = []
        self.success_stories = []
        self.assigned_advocate = ""
        self.resolution = ""
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "human_right": self.human_right_affected,
            "ai_system": self.ai_system,
            "severity": self.severity,
            "status": self.status,
            "people_affected": self.people_affected,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M"),
            "advocacy_actions": len(self.advocacy_actions),
            "resolution": self.resolution
        }

class HumanRightsViolation:
    def __init__(self, violation_id: str, right: str, ai_system: str, 
                 description: str, region: str, evidence_level: str):
        self.id = violation_id
        self.right = right
        self.ai_system = ai_system
        self.description = description
        self.region = region
        self.evidence_level = evidence_level  # "documented", "suspected", "verified"
        self.reported_date = datetime.datetime.now()
        self.status = "active"
        self.related_cases = []
        
# Human Rights Framework
HUMAN_RIGHTS = [
    "Right to Privacy",
    "Right to Non-discrimination",
    "Right to Freedom of Expression",
    "Right to Fair Trial",
    "Right to Work",
    "Right to Health",
    "Right to Education",
    "Right to Cultural Participation",
    "Right to Political Participation",
    "Right to Security"
]

# AI Systems affecting human rights
AI_SYSTEMS = [
    "Facial Recognition",
    "Predictive Policing",
    "Social Media Algorithms",
    "Automated Hiring",
    "Healthcare Diagnostics AI",
    "Educational Assessment AI",
    "Credit Scoring Algorithms",
    "Content Moderation AI",
    "Autonomous Weapons",
    "Surveillance Systems"
]

# Advocacy Actions Database
ADVOCACY_ACTIONS = {
    "Legal": [
        "File human rights complaint with UN",
        "Initiate class action lawsuit",
        "Submit to national human rights commission",
        "Request judicial review",
        "File amicus curiae brief"
    ],
    "Policy": [
        "Draft legislation for AI regulation",
        "Propose ethical AI guidelines",
        "Lobby for algorithmic accountability laws",
        "Advocate for AI impact assessments",
        "Push for transparency requirements"
    ],
    "Public Awareness": [
        "Launch public awareness campaign",
        "Organize community workshops",
        "Create educational materials",
        "Host public forums",
        "Develop media partnerships"
    ],
    "Technical": [
        "Develop bias detection tools",
        "Create algorithmic auditing framework",
        "Design privacy-preserving alternatives",
        "Build explainable AI interfaces",
        "Create human-centered design guidelines"
    ],
    "Corporate Engagement": [
        "Demand algorithmic transparency reports",
        "Request human rights impact assessments",
        "Propose ethical review boards",
        "Advocate for user consent mechanisms",
        "Push for grievance redressal systems"
    ]
}

# Success Stories Database
SUCCESS_STORIES = [
    {
        "title": "Banned Discriminatory Hiring AI",
        "description": "Successfully advocated for removal of biased AI that discriminated against women in tech hiring",
        "people_impacted": "5000+ job seekers",
        "year": 2023
    },
    {
        "title": "Transparency in Facial Recognition",
        "description": "Forced government to disclose facial recognition usage in public spaces",
        "people_impacted": "2 million citizens",
        "year": 2022
    },
    {
        "title": "Healthcare AI Accountability",
        "description": "Established oversight committee for medical diagnostic AI systems",
        "people_impacted": "Healthcare patients nationwide",
        "year": 2023
    }
]

# Sidebar
with st.sidebar:
    st.markdown('<div class="human-card">', unsafe_allow_html=True)
    st.title("🤝 Human AI Advocate")
    st.markdown("Protecting human dignity in the age of AI")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 Human Impact Stats")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cases Active", len(st.session_state.advocacy_cases))
    with col2:
        st.metric("People Protected", st.session_state.impact_metrics['people_protected'])
    
    st.markdown("---")
    
    # Report New Issue
    st.subheader("🚨 Report New Issue")
    
    if st.button("📝 Report Human Rights Violation", use_container_width=True):
        st.session_state.reporting_mode = True
        st.rerun()
    
    if st.button("🆕 Generate Test Case", use_container_width=True):
        # Generate a test case
        case_id = f"HUM-{len(st.session_state.advocacy_cases) + 1000}"
        rights = random.choice(HUMAN_RIGHTS)
        systems = random.choice(AI_SYSTEMS)
        
        test_cases = [
            f"Discriminatory {systems} affecting {rights}",
            f"Privacy violation by {systems}",
            f"Lack of transparency in {systems} impacting {rights}",
            f"Algorithmic bias in {systems} violating {rights}"
        ]
        
        new_case = HumanAdvocacyCase(
            case_id=case_id,
            title=random.choice(test_cases),
            description=f"Documented case where {systems} system is negatively impacting {rights}. Evidence shows systematic violation affecting vulnerable populations.",
            human_right_affected=rights,
            ai_system=systems,
            severity=random.choice(["critical", "high", "medium", "low"])
        )
        
        st.session_state.advocacy_cases.append(new_case)
        st.success("Test case generated!")
        st.rerun()
    
    st.markdown("---")
    
    # User Role
    st.subheader("👤 Your Role")
    user_role = st.selectbox(
        "Select your advocacy role:",
        ["Human Rights Advocate", "Legal Expert", "Policy Maker", 
         "Affected Individual", "Researcher", "Concerned Citizen"]
    )
    
    st.info(f"Role: {user_role}")

# Main App
st.markdown('<h1 style="text-align: center; color: #1a73e8;">🤝 Human AI Advocate Platform</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem;">Protecting Human Dignity in Artificial Intelligence Systems</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", 
    "🔍 Cases", 
    "⚖️ Advocacy Toolkit", 
    "📈 Impact Tracker", 
    "💬 Human-Centered AI Chat"
])

with tab1:  # Dashboard
    st.subheader("🌍 Global Human Rights & AI Dashboard")
    
    # Real-time alerts
    if st.session_state.advocacy_cases:
        critical_cases = [c for c in st.session_state.advocacy_cases if c.severity == "critical"]
        if critical_cases:
            st.markdown(f'<div class="urgent-alert">🚨 {len(critical_cases)} CRITICAL human rights cases need immediate attention!</div>', unsafe_allow_html=True)
    
    # Human Impact Metrics
    st.subheader("📊 Human Impact Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="human-metric">', unsafe_allow_html=True)
        st.metric("👥 People Protected", f"{st.session_state.impact_metrics['people_protected']:,}+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="human-metric">', unsafe_allow_html=True)
        st.metric("📜 Policies Influenced", f"{st.session_state.impact_metrics['policies_influenced']}+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="human-metric">', unsafe_allow_html=True)
        st.metric("📣 Awareness Campaigns", f"{st.session_state.impact_metrics['awareness_campaigns']}+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="human-metric">', unsafe_allow_html=True)
        st.metric("⚖️ Legal Interventions", f"{st.session_state.impact_metrics['legal_interventions']}+")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Current Hotspots
    st.subheader("🔥 Current Human Rights Hotspots")
    
    hotspots_data = pd.DataFrame({
        'Region': ['EU', 'USA', 'China', 'India', 'Brazil', 'Africa'],
        'Active Cases': [12, 8, 15, 10, 7, 9],
        'Most Affected Right': ['Privacy', 'Non-discrimination', 'Expression', 'Privacy', 'Work', 'Health']
    })
    
    st.dataframe(hotspots_data, use_container_width=True)
    
    # Success Stories
    st.subheader("🌟 Recent Success Stories")
    
    for story in SUCCESS_STORIES[:2]:
        st.markdown(f'''
        <div class="success-story">
            <h4>✅ {story['title']}</h4>
            <p>{story['description']}</p>
            <p><strong>Impact:</strong> {story['people_impacted']} | <strong>Year:</strong> {story['year']}</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Live Updates Feed
    st.subheader("🔄 Live Human Rights Updates")
    
    updates = [
        {"time": "Just now", "update": "New legislation proposed for AI transparency in healthcare"},
        {"time": "5 min ago", "update": "Community forum organized on algorithmic bias"},
        {"time": "1 hour ago", "update": "UN committee reviews AI human rights guidelines"},
        {"time": "3 hours ago", "update": "Major tech company agrees to human rights audit"}
    ]
    
    for update in updates:
        st.info(f"🕒 {update['time']}: {update['update']}")

with tab2:  # Cases
    st.subheader("📋 Human Rights Advocacy Cases")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_right = st.selectbox("Filter by Human Right", ["All"] + HUMAN_RIGHTS)
    with col2:
        filter_severity = st.selectbox("Filter by Severity", ["All", "critical", "high", "medium", "low"])
    with col3:
        filter_status = st.selectbox("Filter by Status", ["All", "reported", "investigating", "advocating", "resolved"])
    
    # Cases Display
    filtered_cases = st.session_state.advocacy_cases
    
    if filter_right != "All":
        filtered_cases = [c for c in filtered_cases if c.human_right_affected == filter_right]
    if filter_severity != "All":
        filtered_cases = [c for c in filtered_cases if c.severity == filter_severity]
    if filter_status != "All":
        filtered_cases = [c for c in filtered_cases if c.status == filter_status]
    
    if filtered_cases:
        for case in filtered_cases:
            # Determine color based on severity
            severity_colors = {
                "critical": "#d32f2f",
                "high": "#f57c00",
                "medium": "#1976d2",
                "low": "#388e3c"
            }
            
            st.markdown(f'''
            <div style="border-left: 5px solid {severity_colors[case.severity]}; 
                        padding: 15px; margin: 10px 0; background: white; border-radius: 5px;">
                <h4>{case.title} <span style="color: {severity_colors[case.severity]}; 
                    font-weight: bold;">[{case.severity.upper()}]</span></h4>
                <p><strong>Human Right:</strong> {case.human_right_affected} | 
                <strong>AI System:</strong> {case.ai_system}</p>
                <p><strong>People Affected:</strong> {case.people_affected:,} | 
                <strong>Status:</strong> {case.status}</p>
                <p>{case.description[:200]}...</p>
            </div>
            ''', unsafe_allow_html=True)
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
            with col_btn1:
                if st.button("🔍 Investigate", key=f"invest_{case.id}"):
                    st.session_state.selected_case = case.id
                    st.rerun()
            with col_btn2:
                if st.button("🤝 Advocate", key=f"adv_{case.id}"):
                    st.session_state.advocacy_mode = case.id
                    st.rerun()
            with col_btn3:
                if case.assigned_advocate:
                    st.info(f"Assigned to: {case.assigned_advocate}")
                else:
                    if st.button("👤 Take This Case", key=f"take_{case.id}"):
                        case.assigned_advocate = user_role
                        st.success(f"Case assigned to {user_role}!")
                        st.rerun()
    else:
        st.info("No cases match your filters. Try generating a test case or adjusting filters.")
    
    # Case Details View
    if 'selected_case' in st.session_state:
        case_id = st.session_state.selected_case
        case = next((c for c in st.session_state.advocacy_cases if c.id == case_id), None)
        
        if case:
            st.markdown("---")
            st.subheader("🔍 Case Details")
            
            col_detail1, col_detail2 = st.columns([2, 1])
            
            with col_detail1:
                st.markdown(f"### {case.title}")
                st.markdown(f"**Case ID:** {case.id}")
                st.markdown(f"**Human Right Affected:** {case.human_right_affected}")
                st.markdown(f"**AI System:** {case.ai_system}")
                st.markdown(f"**Severity:** {case.severity}")
                st.markdown(f"**People Affected:** {case.people_affected:,}")
                st.markdown(f"**Status:** {case.status}")
                st.markdown(f"**Reported:** {case.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                st.markdown("---")
                st.markdown("#### 📝 Description")
                st.write(case.description)
                
                if case.advocacy_actions:
                    st.markdown("#### ⚡ Advocacy Actions Taken")
                    for action in case.advocacy_actions:
                        st.info(f"• {action}")
                
                if case.resolution:
                    st.markdown("#### ✅ Resolution")
                    st.success(case.resolution)
            
            with col_detail2:
                st.markdown("#### 🛠️ Take Action")
                
                # Update Status
                new_status = st.selectbox("Update Status", 
                                         ["reported", "investigating", "advocating", "resolved"],
                                         index=["reported", "investigating", "advocating", "resolved"].index(case.status))
                if new_status != case.status:
                    case.status = new_status
                    st.success(f"Status updated to {new_status}")
                
                # Add Advocacy Action
                st.markdown("##### Add Advocacy Action")
                action_type = st.selectbox("Action Type", list(ADVOCACY_ACTIONS.keys()))
                if action_type:
                    selected_action = st.selectbox("Select Action", ADVOCACY_ACTIONS[action_type])
                    if st.button("Add Action"):
                        case.advocacy_actions.append(selected_action)
                        st.success(f"Added: {selected_action}")
                        
                        # Update metrics
                        if "legal" in selected_action.lower():
                            st.session_state.impact_metrics['legal_interventions'] += 1
                        elif "campaign" in selected_action.lower():
                            st.session_state.impact_metrics['awareness_campaigns'] += 1
                
                # Resolution
                st.markdown("##### Record Resolution")
                resolution_text = st.text_area("Resolution details:", case.resolution)
                if resolution_text != case.resolution:
                    case.resolution = resolution_text
                    if resolution_text:
                        case.status = "resolved"
                        st.session_state.impact_metrics['people_protected'] += case.people_affected
                
                if st.button("Save Resolution"):
                    st.success("Resolution saved!")

with tab3:  # Advocacy Toolkit
    st.subheader("⚖️ Human-Centered Advocacy Toolkit")
    
    col_tool1, col_tool2 = st.columns(2)
    
    with col_tool1:
        st.markdown("### 🎯 Strategy Builder")
        
        target_right = st.selectbox("Select Human Right to Protect:", HUMAN_RIGHTS)
        target_ai = st.selectbox("Target AI System:", AI_SYSTEMS)
        
        st.markdown("#### 📋 Recommended Actions")
        
        # Generate recommended actions based on selection
        recommendations = {
            "Right to Privacy": ["Legal", "Policy", "Public Awareness"],
            "Right to Non-discrimination": ["Legal", "Technical", "Corporate Engagement"],
            "Right to Freedom of Expression": ["Policy", "Public Awareness", "Corporate Engagement"],
            "Right to Health": ["Policy", "Technical", "Corporate Engagement"]
        }
        
        rec_type = recommendations.get(target_right, ["Legal", "Policy"])
        
        for action_type in rec_type[:2]:
            with st.expander(f"{action_type} Actions"):
                for action in ADVOCACY_ACTIONS[action_type]:
                    if st.checkbox(action):
                        st.info(f"Selected: {action}")
        
        if st.button("📋 Generate Advocacy Plan"):
            st.success(f"Advocacy plan generated for protecting {target_right} against {target_ai}!")
    
    with col_tool2:
        st.markdown("### 📚 Resource Library")
        
        resources = {
            "Legal Templates": [
                "Human Rights Complaint Template",
                "Algorithmic Impact Assessment Guide",
                "Transparency Request Letter",
                "Legal Demand Letter"
            ],
            "Policy Tools": [
                "AI Regulation Framework",
                "Ethical Guidelines Checklist",
                "Stakeholder Engagement Plan",
                "Impact Assessment Methodology"
            ],
            "Community Tools": [
                "Public Awareness Campaign Kit",
                "Community Workshop Guide",
                "Social Media Toolkit",
                "Petition Template"
            ],
            "Technical Resources": [
                "Bias Detection Framework",
                "Privacy Impact Assessment",
                "Algorithmic Audit Guide",
                "Human-Centered Design Principles"
            ]
        }
        
        for category, items in resources.items():
            with st.expander(f"📁 {category}"):
                for item in items:
                    if st.button(f"📄 {item}", key=f"res_{item}"):
                        st.info(f"Downloading {item}...")
        
        st.markdown("---")
        st.markdown("### 🌐 International Frameworks")
        
        frameworks = [
            "UN Guiding Principles on Business & Human Rights",
            "OECD AI Principles",
            "EU AI Act Guidelines",
            "Universal Declaration of Human Rights"
        ]
        
        for framework in frameworks:
            st.write(f"• {framework}")

with tab4:  # Impact Tracker
    st.subheader("📈 Human Impact Tracker")
    
    # Impact Visualization
    if st.session_state.advocacy_cases:
        cases_df = pd.DataFrame([c.to_dict() for c in st.session_state.advocacy_cases])
        
        col_imp1, col_imp2 = st.columns(2)
        
        with col_imp1:
            st.markdown("### 👥 People Impacted by Right")
            right_counts = cases_df.groupby('human_right')['people_affected'].sum().sort_values(ascending=False)
            st.bar_chart(right_counts)
        
        with col_imp2:
            st.markdown("### ⚖️ Cases by AI System")
            system_counts = cases_df['ai_system'].value_counts()
            st.bar_chart(system_counts)
        
        # Cumulative Impact
        st.markdown("### 📊 Cumulative Human Impact")
        
        # Simulate impact growth over time
        impact_timeline = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'People Protected': [1000, 5000, 15000, 30000, 45000, 60000],
            'Policies Influenced': [0, 1, 3, 5, 8, 12],
            'Legal Interventions': [0, 2, 5, 8, 12, 15]
        })
        
        st.line_chart(impact_timeline.set_index('Month'))
        
        # Success Metrics
        st.markdown("### 🎯 Your Advocacy Impact")
        
        user_cases = [c for c in st.session_state.advocacy_cases if c.assigned_advocate == user_role]
        
        if user_cases:
            col_u1, col_u2, col_u3 = st.columns(3)
            with col_u1:
                st.metric("Your Cases", len(user_cases))
            with col_u2:
                total_impact = sum(c.people_affected for c in user_cases)
                st.metric("People Impacted", f"{total_impact:,}")
            with col_u3:
                resolved = len([c for c in user_cases if c.status == "resolved"])
                st.metric("Cases Resolved", resolved)
        else:
            st.info("Take on cases to build your impact profile!")
    
    # Global Impact Map
    st.markdown("### 🌍 Global Human Rights & AI Landscape")
    
    global_data = pd.DataFrame({
        'Region': ['North America', 'Europe', 'Asia', 'Africa', 'South America'],
        'Active Cases': [25, 32, 45, 18, 22],
        'Most Violated Right': ['Privacy', 'Non-discrimination', 'Expression', 'Health', 'Work'],
        'Advocacy Success Rate': ['65%', '72%', '45%', '58%', '62%']
    })
    
    st.dataframe(global_data, use_container_width=True)

with tab5:  # Human-Centered AI Chat
    st.subheader("💬 Human-Centered AI Advisory Chat")
    
    st.markdown("""
    <div class="advocacy-action">
        <h4>🤖 AI Assistant for Human Rights Advocacy</h4>
        <p>Ask questions about human rights protections, advocacy strategies, or get guidance on specific cases.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message['sender'] == 'user':
                st.markdown(f'<div class="chat-human"><strong>You:</strong> {message["text"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><strong>AI Advocate:</strong> {message["text"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    user_input = st.text_input("Ask about human rights and AI:", key="chat_input")
    
    col_chat1, col_chat2 = st.columns([4, 1])
    with col_chat1:
        if st.button("Send Message", use_container_width=True):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({
                    'sender': 'user',
                    'text': user_input,
                    'time': datetime.datetime.now().strftime("%H:%M")
                })
                
                # Generate AI response
                ai_responses = {
                    "human rights": "Human rights in AI include privacy, non-discrimination, and freedom from automated decision-making harm. Which specific right concerns you?",
                    "privacy": "For privacy violations, consider: 1) Documenting the breach 2) Filing complaint with data protection authority 3) Demanding algorithmic transparency",
                    "discrimination": "Algorithmic discrimination requires: 1) Collecting evidence of bias 2) Requesting impact assessment 3) Engaging affected communities 4) Legal action if systemic",
                    "advocacy": "Effective advocacy involves: 1) Building coalitions 2) Using multiple channels (legal, media, policy) 3) Centering affected voices 4) Demanding accountability",
                    "transparency": "For transparency issues: 1) File freedom of information requests 2) Demand explainability of AI decisions 3) Advocate for public algorithmic audits",
                    "legal": "Legal options include: 1) Human rights complaints 2) Class action lawsuits 3) Regulatory petitions 4) International human rights mechanisms"
                }
                
                # Find relevant response
                ai_response = "I understand you're concerned about human rights and AI. Could you specify which aspect you'd like to discuss?"
                for keyword, response in ai_responses.items():
                    if keyword in user_input.lower():
                        ai_response = response
                        break
                
                # Add AI response
                st.session_state.chat_history.append({
                    'sender': 'ai',
                    'text': ai_response,
                    'time': datetime.datetime.now().strftime("%H:%M")
                })
                
                st.rerun()
    
    with col_chat2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    # Quick questions
    st.markdown("#### 💡 Quick Questions")
    
    quick_questions = [
        "How to report AI privacy violation?",
        "What are my rights against algorithmic bias?",
        "How to start an advocacy campaign?",
        "Legal options for AI discrimination?"
    ]
    
    cols = st.columns(len(quick_questions))
    for idx, question in enumerate(quick_questions):
        with cols[idx]:
            if st.button(question, key=f"qq_{idx}"):
                st.session_state.chat_history.append({
                    'sender': 'user',
                    'text': question,
                    'time': datetime.datetime.now().strftime("%H:%M")
                })
                
                # Add predefined response
                responses = [
                    "To report privacy violations: 1) Document evidence 2) Contact data protection authority 3) File formal complaint",
                    "Your rights include: non-discrimination, explanation of decisions, human oversight, and recourse mechanisms",
                    "Start with: 1) Identify issue 2) Gather evidence 3) Build coalition 4) Choose advocacy channels 5) Track impact",
                    "Legal options: 1) Discrimination lawsuits 2) Human rights complaints 3) Regulatory enforcement 4) Public interest litigation"
                ]
                
                st.session_state.chat_history.append({
                    'sender': 'ai',
                    'text': responses[idx],
                    'time': datetime.datetime.now().strftime("%H:%M")
                })
                
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; padding: 20px; color: #666;'>
    <h4>🤝 Human AI Advocate Platform</h4>
    <p>Protecting human dignity in the age of artificial intelligence</p>
    <p>Need help? Contact: human-rights@ai-advocate.org | Emergency Hotline: 1-888-AI-HUMAN</p>
    <p style='font-size: 0.9rem;'>Built with ❤️ for a human-centered AI future</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Real-time updates
if st.checkbox("🔄 Enable live updates", value=False):
    st.info("Live updates enabled - monitoring human rights developments...")
    time.sleep(10)
    st.rerun()
