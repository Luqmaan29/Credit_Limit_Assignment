"""
Credit Limit Assignment System - Streamlit Dashboard
Main application for credit limit recommendations and analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import custom modules
from data_generator import generate_credit_dataset
from model_training import CreditRiskModel
from credit_limit_engine import CreditLimitEngine
from scenario_analysis import ScenarioAnalyzer

# Page configuration
st.set_page_config(
    page_title="Credit Limit Assignment System - Indian Market",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and prepare the credit data"""
    try:
        df = pd.read_csv('data/credit_data.csv')
    except FileNotFoundError:
        st.error("Data file not found. Please run 'python data_generator.py' first.")
        return None
    
    return df

@st.cache_resource
def load_models():
    """Load trained ML models"""
    model = CreditRiskModel()
    try:
        model.load_models()
        return model
    except FileNotFoundError:
        st.warning("Models not found. Training models...")
        df = load_data()
        if df is not None:
            model.train_models(df)
            model.save_models()
            return model
        return None

def main():
    st.markdown('<h1 class="main-header">💳 Dynamic Credit Limit Assignment System - India</h1>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Sidebar
    st.sidebar.header("⚙️ Settings")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Select Page",
        ["💻 Personal Credit Calculator", "📊 Overview", "🎯 Credit Recommendations", "📈 Risk Analysis", 
         "🌍 Scenario Analysis", "🔍 Customer Details"]
    )
    
    # Apply model predictions
    model = load_models()
    if model is None:
        return
    
    with st.spinner("Generating predictions..."):
        df['predicted_default_prob'] = model.predict_default_probability(df)
    
    # Main content based on selected page
    if page == "💻 Personal Credit Calculator":
        show_personal_calculator()
    elif page == "📊 Overview":
        show_overview(df)
    elif page == "🎯 Credit Recommendations":
        show_recommendations(df)
    elif page == "📈 Risk Analysis":
        show_risk_analysis(df)
    elif page == "🌍 Scenario Analysis":
        show_scenario_analysis(df)
    elif page == "🔍 Customer Details":
        show_customer_details(df)

def show_personal_calculator():
    """Interactive form for users to input their details and get credit limit recommendation"""
    st.header("💻 Personal Credit Limit Calculator")
    
    st.markdown("### Calculate your ideal credit card limit based on your financial profile")
    st.info("💡 **Simple & Free**: Enter your details below to get instant credit limit recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👤 About You")
        age = st.number_input("Your Age", min_value=18, max_value=75, value=30, step=1,
                              help="Your current age")
        monthly_income = st.number_input("Monthly Salary/Income (₹)", min_value=15000, max_value=500000, 
                                          value=50000, step=5000,
                                          help="Your total monthly income from all sources")
        cibil_score = st.number_input("Credit Score (CIBIL)", min_value=300, max_value=900, value=700, step=1,
                                     help="Your CIBIL/credit score (300-900 range)")
        
    with col2:
        st.subheader("💳 Your Current Credit Card")
        current_limit = st.number_input("Current Credit Card Limit (₹)", min_value=10000, max_value=500000,
                                        value=75000, step=5000,
                                        help="How much credit limit do you currently have?")
        utilization = st.slider("How much do you use? (%)", min_value=0, max_value=100, value=30, step=5,
                               help="What percentage of your credit limit do you use on average?") / 100
        on_time_rate = st.slider("How often do you pay on time? (%)", min_value=0, max_value=100, value=95, step=5,
                                help="What percentage of bills do you pay on time?") / 100
    
    # Additional details
    st.subheader("📝 More Details About Your Finances")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        months_open = st.number_input("How long have you had credit cards? (months)", min_value=1, max_value=120, 
                                     value=24, step=1,
                                     help="How many months have you been using credit cards?")
        late_payments = st.number_input("Late payments in last year", min_value=0, max_value=12, value=0, step=1,
                                       help="How many times did you pay late in the last 12 months?")
    
    with col2:
        st.markdown("**Any Serious Financial Issues?**")
        has_bankruptcy = st.checkbox("Have you ever filed for bankruptcy?")
        has_delinquency = st.checkbox("Have you ever had a loan defaulted or written off?")
    
    with col3:
        debt_to_income = st.slider("Monthly debt payments (% of income)", min_value=0, max_value=90, value=30, step=5,
                                  help="What percentage of your income goes to debt payments (EMIs, loans)?") / 100
    
    # Calculate button
    if st.button("🚀 Get My Recommended Credit Limit", type="primary", use_container_width=True):
        # Prepare data for calculation
        payment_history_score = on_time_rate * 0.8  # Simplified
        
        # Calculate behavior score
        behavior_score = (
            payment_history_score * 0.4 + 
            on_time_rate * 0.3 + 
            (1 - utilization) * 0.2 + 
            (cibil_score / 900) * 0.1
        )
        behavior_score = max(0, min(1, behavior_score))
        
        # Predict default probability
        default_prob = (
            0.3 * (1 - behavior_score) +
            0.25 * (1 - cibil_score / 900) +
            0.2 * utilization +
            0.15 * (debt_to_income / 0.5) +
            0.05 * has_bankruptcy +
            0.05 * has_delinquency
        )
        default_prob = max(0, min(1, default_prob))
        
        # Calculate recommended limit
        engine = CreditLimitEngine()
        
        # Calculate base limit
        if cibil_score >= 750:
            score_multiplier = 1.5
        elif cibil_score >= 700:
            score_multiplier = 1.3
        elif cibil_score >= 650:
            score_multiplier = 1.1
        elif cibil_score >= 550:
            score_multiplier = 1.0
        elif cibil_score >= 450:
            score_multiplier = 0.8
        else:
            score_multiplier = 0.5
        
        base_limit = monthly_income * 2.5 * score_multiplier
        
        # Apply risk adjustment
        risk_multiplier = 1 - (default_prob * 0.6)
        
        if utilization > 0.8:
            risk_multiplier *= 0.9
        elif utilization < 0.3:
            risk_multiplier *= 1.1
        
        risk_multiplier += on_time_rate * 0.1
        risk_multiplier += behavior_score * 0.1
        risk_multiplier = max(0.2, min(2.0, risk_multiplier))
        
        recommended_limit = base_limit * risk_multiplier
        recommended_limit = max(10000, min(recommended_limit, 500000))
        
        change_amount = recommended_limit - current_limit
        change_pct = (change_amount / current_limit) * 100
        
        # Determine risk category
        if default_prob < 0.1:
            risk_category = "Low Risk"
            risk_color = "green"
        elif default_prob < 0.25:
            risk_category = "Medium Risk"
            risk_color = "orange"
        elif default_prob < 0.4:
            risk_category = "High Risk"
            risk_color = "red"
        else:
            risk_category = "Very High Risk"
            risk_color = "darkred"
        
        # Display results
        st.divider()
        st.header("📊 Your Credit Limit Recommendation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Current Limit", f"₹{current_limit:,.0f}")
        
        with col2:
            st.metric("Recommended Limit", f"₹{recommended_limit:,.0f}", 
                     delta=f"₹{change_amount:,.0f} ({change_pct:+.1f}%)")
        
        with col3:
            st.markdown(f"### Risk Category: <span style='color:{risk_color}'>{risk_category}</span>", 
                       unsafe_allow_html=True)
        
        st.divider()
        
        # Detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Your Financial Summary")
            st.write(f"**Credit Score**: {cibil_score}")
            st.write(f"**Monthly Income**: ₹{monthly_income:,.0f}")
            st.write(f"**Credit Usage**: {utilization*100:.1f}%")
            st.write(f"**Payment on Time**: {on_time_rate*100:.1f}%")
            st.write(f"**Risk Level**: {default_prob*100:.2f}% chance of default")
        
        with col2:
            st.subheader("💡 Why This Recommendation?")
            
            reasons = []
            if cibil_score >= 750:
                reasons.append("⭐ Your credit score is excellent (750+)")
            elif cibil_score >= 700:
                reasons.append("👍 Your credit score is very good (700+)")
            elif cibil_score < 550:
                reasons.append("⚠️ Your credit score is quite low")
            
            if on_time_rate > 0.95:
                reasons.append("⭐ You almost always pay on time")
            elif on_time_rate > 0.9:
                reasons.append("👍 You pay most bills on time")
            elif on_time_rate < 0.7:
                reasons.append("⚠️ You miss payments frequently")
            
            if utilization < 0.3:
                reasons.append("⭐ You use credit wisely (low usage)")
            elif utilization > 0.8:
                reasons.append("⚠️ You're using too much of your available credit")
            
            if behavior_score > 0.8:
                reasons.append("👍 You have good overall financial behavior")
            
            if debt_to_income > 0.6:
                reasons.append("⚠️ You're paying a lot towards debts")
            
            if has_bankruptcy:
                reasons.append("⚠️ Past bankruptcy affects your creditworthiness")
            
            if has_delinquency:
                reasons.append("⚠️ Past loan defaults are a concern")
            
            for reason in reasons:
                st.write(reason)
        
        # Visual indicator
        st.divider()
        st.subheader("📊 Current vs Recommended")
        
        fig = go.Figure()
        fig.add_bar(x=['Current', 'Recommended'], 
                   y=[current_limit, recommended_limit],
                   marker_color=['orange', 'green'])
        fig.update_layout(yaxis_title="Credit Limit (₹)", height=300)
        st.plotly_chart(fig, use_container_width=True)

def show_overview(df):
    """Display overview dashboard"""
    st.header("📊 Portfolio Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_customers = len(df)
    avg_credit_score = df['credit_score'].mean()
    avg_utilization = df['credit_utilization'].mean() * 100
    avg_default_prob = df['predicted_default_prob'].mean() * 100
    
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Avg Credit Score", f"{avg_credit_score:.0f}")
    col3.metric("Avg Utilization", f"{avg_utilization:.1f}%")
    col4.metric("Avg Default Risk", f"{avg_default_prob:.2f}%")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Credit Score Distribution")
        fig = px.histogram(df, x='credit_score', nbins=30,
                          labels={'credit_score': 'Credit Score', 'count': 'Number of Customers'},
                          color_discrete_sequence=['#1f77b4'])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Credit Utilization Distribution")
        fig = px.histogram(df, x='credit_utilization', nbins=30,
                          labels={'credit_utilization': 'Credit Utilization', 'count': 'Number of Customers'},
                          color_discrete_sequence=['#2ca02c'])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Default Risk Categories")
        df['risk_category'] = pd.cut(df['predicted_default_prob'], 
                                     bins=[0, 0.15, 0.3, 0.5, 1.0],
                                     labels=['Low', 'Medium', 'High', 'Very High'])
        risk_counts = df['risk_category'].value_counts().sort_index()
        
        fig = px.bar(x=risk_counts.index, y=risk_counts.values,
                    labels={'x': 'Risk Category', 'y': 'Number of Customers'},
                    color=risk_counts.values,
                    color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Economic Scenario Breakdown")
        scenario_map = {0: 'Normal (Moderate Growth)', 1: 'Slowdown', 2: 'High Growth'}
        df['scenario_label'] = df['economic_scenario'].map(scenario_map)
        scenario_counts = df['scenario_label'].value_counts()
        
        fig = px.pie(values=scenario_counts.values, names=scenario_counts.index,
                    hole=0.4)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk-return scatter plot
    st.subheader("Risk vs Current Credit Limit")
    fig = px.scatter(df, x='credit_utilization', y='current_credit_limit',
                    size='predicted_default_prob', color='credit_score',
                    hover_data=['customer_id', 'predicted_default_prob'],
                    labels={'credit_utilization': 'Credit Utilization',
                           'current_credit_limit': 'Current Credit Limit (₹)',
                           'predicted_default_prob': 'Default Probability',
                           'credit_score': 'CIBIL Score'},
                    color_continuous_scale='RdYlGn')
    st.plotly_chart(fig, use_container_width=True, height=500)

def show_recommendations(df):
    """Display credit limit recommendations"""
    st.header("🎯 Credit Limit Recommendations")
    
    # Calculate recommendations
    engine = CreditLimitEngine()
    df['recommended_limit'] = df.apply(
        lambda row: engine.calculate_recommended_limit({
            'monthly_income': row['monthly_income'],
            'credit_score': row['credit_score'],
            'predicted_default_prob': row['predicted_default_prob'],
            'credit_utilization': row['credit_utilization'],
            'on_time_payment_rate': row['on_time_payment_rate'],
            'behavior_score': row['behavior_score']
        }),
        axis=1
    )
    
    df['change_amount'] = df['recommended_limit'] - df['current_credit_limit']
    df['change_percentage'] = (df['change_amount'] / df['current_credit_limit']) * 100
    df['risk_category'] = df['predicted_default_prob'].apply(engine.assign_risk_category)
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_filter = st.multiselect("Filter by Risk Category", 
                                     df['risk_category'].unique(),
                                     default=df['risk_category'].unique())
    with col2:
        change_filter = st.selectbox("Credit Change Filter",
                                    ["All", "Increase Only", "Decrease Only", "No Change"])
    with col3:
        score_threshold = st.slider("Min Credit Score", 
                                    int(df['credit_score'].min()),
                                    int(df['credit_score'].max()),
                                    int(df['credit_score'].min()))
    
    # Apply filters
    filtered_df = df[df['risk_category'].isin(risk_filter)]
    filtered_df = filtered_df[filtered_df['credit_score'] >= score_threshold]
    
    if change_filter == "Increase Only":
        filtered_df = filtered_df[filtered_df['change_amount'] > 0]
    elif change_filter == "Decrease Only":
        filtered_df = filtered_df[filtered_df['change_amount'] < 0]
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Recommended", len(filtered_df))
    col2.metric("Avg Current Limit", f"₹{filtered_df['current_credit_limit'].mean():,.0f}")
    col3.metric("Avg Recommended", f"₹{filtered_df['recommended_limit'].mean():,.0f}")
    col4.metric("Total Exposure Change", 
                f"₹{filtered_df['change_amount'].sum():,.0f}")
    
    # Recommendation table
    display_cols = ['customer_id', 'current_credit_limit', 'recommended_limit',
                   'change_amount', 'change_percentage', 'risk_category',
                   'credit_score', 'predicted_default_prob']
    
    st.subheader("Recommendation Details")
    st.dataframe(
        filtered_df[display_cols].style.format({
            'current_credit_limit': '₹{:,.0f}',
            'recommended_limit': '₹{:,.0f}',
            'change_amount': '₹{:,.0f}',
            'change_percentage': '{:.1f}%',
            'predicted_default_prob': '{:.2%}'
        }),
        use_container_width=True,
        height=400
    )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Credit Limit Changes Distribution")
        fig = px.histogram(filtered_df, x='change_percentage', nbins=40,
                          labels={'change_percentage': 'Change Percentage (%)'},
                          color_discrete_sequence=['#ff7f0e'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Current vs Recommended Limits")
        sample_df = filtered_df.nlargest(30, 'change_amount')[['customer_id', 
                                                              'current_credit_limit',
                                                              'recommended_limit']]
        sample_df = sample_df.melt(id_vars='customer_id', 
                                   value_vars=['current_credit_limit', 'recommended_limit'],
                                   var_name='Type', value_name='Limit')
        
        fig = px.bar(sample_df, x='customer_id', y='Limit', color='Type',
                    barmode='group',
                    labels={'Limit': 'Credit Limit (₹)', 'customer_id': 'Customer ID'})
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def show_risk_analysis(df):
    """Display risk analysis"""
    st.header("📈 Risk Analysis")
    
    # Apply recommendations for risk calculation
    engine = CreditLimitEngine()
    df['recommended_limit'] = df.apply(
        lambda row: engine.calculate_recommended_limit({
            'monthly_income': row['monthly_income'],
            'credit_score': row['credit_score'],
            'predicted_default_prob': row['predicted_default_prob'],
            'credit_utilization': row['credit_utilization'],
            'on_time_payment_rate': row['on_time_payment_rate'],
            'behavior_score': row['behavior_score']
        }),
        axis=1
    )
    
    # Calculate risk metrics
    df['expected_loss'] = df['predicted_default_prob'] * df['recommended_limit']
    df['risk_category'] = df['predicted_default_prob'].apply(engine.assign_risk_category)
    
    # Risk metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_exposure = df['recommended_limit'].sum()
    total_expected_loss = df['expected_loss'].sum()
    avg_risk = df['predicted_default_prob'].mean() * 100
    high_risk_count = len(df[df['predicted_default_prob'] > 0.35])
    
    col1.metric("Total Exposure", f"₹{total_exposure:,.0f}")
    col2.metric("Expected Loss", f"₹{total_expected_loss:,.0f}")
    col3.metric("Average Risk", f"{avg_risk:.2f}%")
    col4.metric("High Risk Customers", f"{high_risk_count}")
    
    st.divider()
    
    # Risk heatmap
    st.subheader("Risk Heatmap: Default Probability vs Credit Limit")
    df['limit_bin'] = pd.cut(df['recommended_limit'], bins=5, labels=['Low', 'Med-Low', 
                                                                       'Medium', 'Med-High', 'High'])
    df['prob_bin'] = pd.cut(df['predicted_default_prob'], bins=5)
    
    heatmap_data = df.groupby(['limit_bin', 'prob_bin']).size().reset_index(name='count')
    heatmap_data = heatmap_data.pivot(index='limit_bin', columns='prob_bin', values='count')
    
    fig = px.imshow(heatmap_data.fillna(0), 
                   labels=dict(x="Default Probability", y="Credit Limit", color="Count"),
                   color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    if st.checkbox("Show Feature Importance"):
        model = load_models()
        if model and model.models_trained:
            importance_df = model.get_feature_importance()
            top_features = importance_df.head(10)
            
            fig = px.bar(top_features, x='avg_importance', y='feature',
                        orientation='h',
                        labels={'avg_importance': 'Average Importance', 'feature': 'Feature'},
                        color='avg_importance',
                        color_continuous_scale='Blues')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

def show_scenario_analysis(df):
    """Display scenario analysis"""
    st.header("🌍 Scenario Analysis")
    
    st.markdown("### Analyze credit limit recommendations under different economic conditions")
    
    # Calculate base recommendations
    engine = CreditLimitEngine()
    df['recommended_limit'] = df.apply(
        lambda row: engine.calculate_recommended_limit({
            'monthly_income': row['monthly_income'],
            'credit_score': row['credit_score'],
            'predicted_default_prob': row['predicted_default_prob'],
            'credit_utilization': row['credit_utilization'],
            'on_time_payment_rate': row['on_time_payment_rate'],
            'behavior_score': row['behavior_score']
        }),
        axis=1
    )
    
    # Run scenario analysis
    analyzer = ScenarioAnalyzer()
    scenario_results = analyzer.analyze_scenarios(df)
    
    # Display results
    st.subheader("Scenario Comparison")
    st.dataframe(scenario_results.style.format({
        'avg_credit_limit': '₹{:,.0f}',
        'total_exposure': '₹{:,.0f}',
        'avg_limit_change_pct': '{:.2f}%',
        'weighted_avg_risk': '{:.2%}'
    }))
    
    # Scenario charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Total Exposure by Scenario")
        fig = px.bar(scenario_results, x='scenario', y='total_exposure',
                    labels={'scenario': 'Scenario', 'total_exposure': 'Total Exposure (₹)'},
                    color='scenario',
                    color_discrete_map={'Normal': '#1f77b4', 
                                       'Slowdown': '#d62728',
                                       'High_Growth': '#2ca02c'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Average Credit Limit by Scenario")
        fig = px.bar(scenario_results, x='scenario', y='avg_credit_limit',
                    labels={'scenario': 'Scenario', 
                           'avg_credit_limit': 'Avg Credit Limit (₹)'},
                    color='scenario',
                    color_discrete_map={'Normal': '#1f77b4',
                                       'Slowdown': '#d62728',
                                       'High_Growth': '#2ca02c'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk by scenario
    st.subheader("Weighted Average Risk by Scenario")
    fig = px.line(scenario_results, x='scenario', y='weighted_avg_risk',
                 markers=True,
                 labels={'scenario': 'Scenario', 
                        'weighted_avg_risk': 'Weighted Avg Risk'})
    fig.update_traces(line_width=3)
    st.plotly_chart(fig, use_container_width=True)
    
    # Get recommendations
    recommendations = analyzer.get_scenario_recommendation(df)
    
    st.subheader("Scenario Recommendations")
    for _, row in recommendations.iterrows():
        with st.expander(f"{row['scenario']} Scenario"):
            st.write(f"**Recommendation:** {row['recommendation']}")
            st.metric("Avg Credit Limit", f"₹{row['avg_credit_limit']:,.0f}")
            st.metric("Total Exposure", f"₹{row['total_exposure']:,.0f}")
            st.metric("Weighted Risk", f"{row['weighted_avg_risk']:.2%}")

def show_customer_details(df):
    """Display detailed customer information"""
    st.header("🔍 Customer Details")
    
    # Search customer
    customer_id = st.selectbox("Select Customer", 
                              ['All'] + sorted(df['customer_id'].unique().tolist()))
    
    if customer_id == 'All':
        search_df = df
    else:
        search_df = df[df['customer_id'] == customer_id]
    
    # Calculate recommendations for displayed customers
    engine = CreditLimitEngine()
    
    def process_row(row):
        rec = engine.calculate_recommended_limit({
            'monthly_income': row['monthly_income'],
            'credit_score': row['credit_score'],
            'predicted_default_prob': row['predicted_default_prob'],
            'credit_utilization': row['credit_utilization'],
            'on_time_payment_rate': row['on_time_payment_rate'],
            'behavior_score': row['behavior_score']
        })
        return rec
    
    search_df = search_df.copy()
    search_df['recommended_limit'] = search_df.apply(process_row, axis=1)
    search_df['change_amount'] = search_df['recommended_limit'] - search_df['current_credit_limit']
    search_df['change_percentage'] = (search_df['change_amount'] / search_df['current_credit_limit']) * 100
    search_df['risk_category'] = search_df['predicted_default_prob'].apply(engine.assign_risk_category)
    
    # Display details
    for idx, row in search_df.iterrows():
        with st.expander(f"{row['customer_id']} - {row['risk_category']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current Status**")
                st.metric("Current Credit Limit", f"₹{row['current_credit_limit']:,.2f}")
                st.metric("CIBIL Score", f"{row['credit_score']}")
                st.metric("Credit Utilization", f"{row['credit_utilization']:.1%}")
                st.metric("Monthly Income", f"₹{row['monthly_income']*1000:,.0f}")
            
            with col2:
                st.markdown("**Recommendations**")
                st.metric("Recommended Limit", f"₹{row['recommended_limit']:,.2f}")
                st.metric("Change Amount", f"₹{row['change_amount']:,.2f}")
                st.metric("Change %", f"{row['change_percentage']:.2f}%")
                st.metric("Default Risk", f"{row['predicted_default_prob']:.2%}")
            
            st.markdown("**Risk Indicators**")
            col1, col2, col3 = st.columns(3)
            col1.metric("On-Time Payment Rate", f"{row['on_time_payment_rate']:.1%}")
            col2.metric("Behavior Score", f"{row['behavior_score']:.3f}")
            col3.metric("Payment History Score", f"{row['payment_history_score']:.3f}")

if __name__ == '__main__':
    main()

