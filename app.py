import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import numpy as np
# streamlit run 筑安云脑安全氛围管理平台.py
# 页面配置
st.set_page_config(
    page_title="筑安云脑安全氛围管理平台",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
<style>
    /* 主背景 - 优雅的渐变色 */
    .main {
        background: linear-gradient(135deg, #f0f4f8 0%, #e8eef5 50%, #dfe7f2 100%);
        position: relative;
    }

    .main::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 30%, rgba(90, 113, 153, 0.04) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(102, 122, 159, 0.04) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    /* 侧边栏样式 - 加深的蓝灰色渐变 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5a7199 0%, #667a9f 50%, #7689ab 100%);
        box-shadow: 2px 0 20px rgba(0, 0, 0, 0.15);
    }

    [data-testid="stSidebar"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, transparent 100%);
        pointer-events: none;
    }

    [data-testid="stSidebar"] .stButton button {
        color: white;
        background-color: transparent;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-size: 15px;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.5);
        transform: translateX(3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, rgba(139, 157, 195, 0.5) 0%, rgba(160, 174, 208, 0.5) 100%);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 4px 12px rgba(139, 157, 195, 0.25);
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2);
        border-width: 1px;
    }

    .main-header {
        font-size: 28px;
        font-weight: bold;
        text-align: left;
        padding: 15px 0;
        color: #3d4f5e;
        margin-bottom: 20px;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }

    /* 指标卡片 - 更丰富的渐变 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 28px rgba(102, 126, 234, 0.4);
    }

    /* 通知框 - 优化玻璃态效果 */
    .notification-box {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 14px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    .notification-box:hover {
        background: rgba(255, 255, 255, 1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        transform: translateX(5px);
    }

    /* 蓝色渐变卡片 - 深度效果 */
    .blue-gradient-card {
        background: linear-gradient(135deg, #5a7fd6 0%, #6b8cd9 50%, #7c6fb8 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 30px rgba(90, 127, 214, 0.3);
        position: relative;
        overflow: hidden;
    }
    .blue-gradient-card::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    /* 白色卡片 - 优化玻璃态设计 */
    .white-card {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.9);
        transition: all 0.3s ease;
    }
    .white-card:hover {
        background: rgba(255, 255, 255, 1);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }

    /* 按钮通用样式 */
    .stButton > button {
        border-radius: 8px;
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        transform: translateY(-2px);
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }

    /* 3D工具栏 - 现代设计 */
    .toolbar-3d {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #3d566e 100%);
        padding: 12px 20px;
        border-radius: 14px;
        display: flex;
        gap: 8px;
        align-items: center;
        justify-content: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .toolbar-button {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: white;
        padding: 8px 12px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 18px;
        min-width: 45px;
        text-align: center;
        backdrop-filter: blur(5px);
    }
    .toolbar-button:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .toolbar-button.active {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(123, 163, 217, 0.7) 100%);
        border-color: rgba(102, 126, 234, 0.8);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.5);
    }

    /* 搜索框美化 */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(90, 113, 153, 0.2);
        border-radius: 10px;
        padding: 12px 15px;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(90, 113, 153, 0.4);
        box-shadow: 0 0 0 3px rgba(90, 113, 153, 0.08);
        background: rgba(255, 255, 255, 1);
    }

    /* 日历美化 */
    .calendar-2025 {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.9);
    }

    /* Plotly图表容器 */
    .js-plotly-plot {
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }

    /* 数据表格美化 */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.97);
        backdrop-filter: blur(10px);
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }

    /* 滚动条美化 */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.03);
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8b9dc3 0%, #a0aed0 100%);
        border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7a8cb3 0%, #8f9dc0 100%);
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = '工作台'
if 'intervention_tab' not in st.session_state:
    st.session_state.intervention_tab = '干预计划'
if 'selected_worker' not in st.session_state:
    st.session_state.selected_worker = '张三'
if 'optimize_checkbox1' not in st.session_state:
    st.session_state.optimize_checkbox1 = False
if 'optimize_checkbox2' not in st.session_state:
    st.session_state.optimize_checkbox2 = False
if 'intervention_data' not in st.session_state:
    st.session_state.intervention_data = []
if 'progress_level' not in st.session_state:
    st.session_state.progress_level = '一级项目'
if 'training_tab' not in st.session_state:
    st.session_state.training_tab = '排行榜'
if 'search_worker_id' not in st.session_state:
    st.session_state.search_worker_id = 'A12011'
if 'camera_zoom' not in st.session_state:
    st.session_state.camera_zoom = 1.6
if 'camera_rotation' not in st.session_state:
    st.session_state.camera_rotation = 0
if 'show_workers' not in st.session_state:
    st.session_state.show_workers = True
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'default'
if 'editing_plan' not in st.session_state:
    st.session_state.editing_plan = None
if 'plan_data' not in st.session_state:
    st.session_state.plan_data = {
        'plan1': {
            'time': '2025-08-05',
            'analysis': '从众心理,回组多人违规',
            'measure': '调离发起者至其他班组',
            'effect': '违规下降37%',
            'result': '即将干预'
        },
        'plan2': {
            'time': '2025-08-03',
            'analysis': '生理疲劳3级',
            'measure': '智能耳机播放提神音效+强制休息',
            'effect': '',
            'result': '待执行'
        }
    }
if 'intervention_records' not in st.session_state:
    st.session_state.intervention_records = []
if 'show_detail_dialog' not in st.session_state:
    st.session_state.show_detail_dialog = False
if 'ignored_workers' not in st.session_state:
    st.session_state.ignored_workers = []
if 'alert_start_date' not in st.session_state:
    st.session_state.alert_start_date = None
if 'alert_end_date' not in st.session_state:
    st.session_state.alert_end_date = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = {}
if 'settings_category' not in st.session_state:
    st.session_state.settings_category = '通用设置'
if 'theme_mode' not in st.session_state:
    st.session_state.theme_mode = '浅色模式'
if 'language' not in st.session_state:
    st.session_state.language = '简体中文'
if 'notification_enabled' not in st.session_state:
    st.session_state.notification_enabled = True
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30
if 'risk_threshold_l1' not in st.session_state:
    st.session_state.risk_threshold_l1 = 30
if 'risk_threshold_l2' not in st.session_state:
    st.session_state.risk_threshold_l2 = 60
if 'risk_threshold_l3' not in st.session_state:
    st.session_state.risk_threshold_l3 = 80

def generate_ai_analysis(worker_name, worker_info, intervention_records):
    """根据工人信息和干预记录生成智能分析"""

    risk_value = worker_info['风险值']
    fatigue = worker_info['疲劳度']
    attention = worker_info['注意力']
    level = worker_info['等级']
    age = worker_info['年龄']
    position = worker_info['职位']

    # 1. 风险评估
    if risk_value > 70:
        risk_assessment = f"⚠️ 高风险：{worker_name}当前风险值{risk_value:.1f}，属于{level}级别，需立即关注"
    elif risk_value > 40:
        risk_assessment = f"⚡ 中风险：{worker_name}风险值{risk_value:.1f}，需要加强监控和预防措施"
    else:
        risk_assessment = f"✅ 低风险：{worker_name}当前状态良好，风险值{risk_value:.1f}，继续保持"

    # 2. 主要关注点
    concerns = []
    if fatigue > 70:
        concerns.append(f"疲劳度过高({fatigue:.1f})")
    if attention < 50:
        concerns.append(f"注意力不集中({attention:.1f})")
    if age > 50:
        concerns.append(f"年龄偏大({age}岁)")
    if level == 'L3':
        concerns.append("高危等级")

    if concerns:
        concern_text = f"🎯 关注点：该工人存在" + "、".join(concerns) + f"等问题，从事{position}工作需特别注意"
    else:
        concern_text = f"🎯 关注点：该工人整体状态稳定，作为{position}表现良好，暂无明显风险因素"

    # 3. 建议措施
    suggestions = []
    if fatigue > 70:
        suggestions.append("安排强制休息")
    if attention < 50:
        suggestions.append("调整至低风险岗位")
    if risk_value > 60:
        suggestions.append("增加安全培训频次")
    if len(intervention_records) > 3:
        suggestions.append("重点监控该工人")
    if age > 50 and risk_value > 50:
        suggestions.append("减少高空作业时间")

    if not suggestions:
        suggestions = ["继续保持良好状态", "定期安全检查", "参加安全培训"]

    suggestion_text = f"💡 建议：" + "；".join(suggestions[:3])

    # 4. 历史记录分析
    if len(intervention_records) > 0:
        record_text = f"\n\n📊 历史记录：已有{len(intervention_records)}次干预记录，建议持续跟踪效果"
    else:
        record_text = f"\n\n📊 历史记录：暂无干预记录，建议建立工人安全档案"

    # 组合结果
    analysis = f"""{risk_assessment}

{concern_text}

{suggestion_text}

{record_text}"""

    return analysis.strip()


@st.cache_data
def generate_mock_data():
    workers = []
    names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
             '小A', '小B', '小C', '小D', '小E', '小F', '小G', '小H', '小I', '小J',
             '刘明', '陈强', '杨帆', '黄伟', '周杰', '吴磊', '郑浩', '王芳', '赵敏', '孙洋',
             '李娜', '陈阳', '张伟', '王静', '刘洋', '杨丽', '周敏', '吴强', '郑宇', '黄磊',
             '赵刚', '孙杰', '李晨', '陈浩', '张敏', '王涛', '刘军', '杨阳', '周霞', '吴明']
    areas = ['乙园区', '甲园区', '丙园区', '丁园区']
    levels = ['L1', 'L2', 'L3']
    positions_list = ['混凝土工', '钢筋工', '架子工', '电焊工', '木工', '抹灰工', '瓦工', '管道工', '电工', '防水工']

    positions = [
        (-25, 30, 2), (15, -20, 3), (-30, -15, 1), (25, 25, 4),
        (5, 10, 2), (-10, -25, 1), (20, 15, 3), (-20, 20, 2),
        (10, -15, 1), (-15, -10, 2), (30, -5, 3), (-5, 25, 1)
    ]

    for i, name in enumerate(names):
        if i < len(positions):
            pos = positions[i]
        else:
            pos = (random.uniform(-30, 30), random.uniform(-30, 30), random.uniform(1, 4))

        # 为每个工人生成预警时间（最近7天内的随机时间）
        alert_time = datetime.now() - timedelta(days=random.randint(0, 7),
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))

        workers.append({
            '工人姓名': name,
            '等级': random.choice(levels),
            '所在区域': random.choice(areas),
            '风险值': random.uniform(0, 100),
            '疲劳度': random.uniform(0, 100),
            '注意力': random.uniform(0, 100),
            '工号': f'A{12011 + i}',
            '年龄': random.randint(25, 55),
            '紧急联系人': f'1{random.randint(30, 89)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}',
            '职位': random.choice(positions_list),
            '位置': pos,
            '预警时间': alert_time
        })

    dates = [(datetime.now() + timedelta(days=i)).strftime('%m月%d日') for i in range(7)]
    risk_values = [11.2, 9.8, 15.1, 12.4, 24.5, 13.6, 7.4]
    level_stable = {'L1': 51.2, 'L2': 14.6, 'L3': 7.0}
    level_unstable = {'L1': 15.7, 'L2': 5.1, 'L3': 6.4}

    return pd.DataFrame(workers), dates, risk_values, level_stable, level_unstable


def search_workers(query, workers_df):
    """真实的搜索功能 - 修复乱码问题"""
    if not query or query.strip() == "":
        return pd.DataFrame()

    query = str(query).strip()

    try:
        results = workers_df[
            workers_df['工人姓名'].astype(str).str.contains(query, case=False, na=False) |
            workers_df['工号'].astype(str).str.contains(query, case=False, na=False) |
            workers_df['所在区域'].astype(str).str.contains(query, case=False, na=False) |
            workers_df['职位'].astype(str).str.contains(query, case=False, na=False) |
            workers_df['等级'].astype(str).str.contains(query, case=False, na=False)
            ]
        return results
    except Exception as e:
        st.error(f"搜索出错: {str(e)}")
        return pd.DataFrame()


def render_sidebar():
    with st.sidebar:
        st.markdown("## 🏢 筑安云脑", unsafe_allow_html=True)
        st.markdown("---")

        # 折叠状态 & 当前子页面
        if "alert_sub_expand" not in st.session_state:
            st.session_state.alert_sub_expand = False
        if "alert_sub_page" not in st.session_state:
            st.session_state.alert_sub_page = None     #  null 表示还没选中子页面

        # 一级菜单配置
        main_menu = {
            "📊 工作台": "工作台",
            "⚠️ 实时预警": "实时预警",   # 特殊处理
            "🎯 干预措施": "干预措施",
            "📈 进度管理": "进度管理",
            "🎓 安全培训": "安全培训",
            "🤖 智能AI助手": "智能AI助手"
        }

        for label, page in main_menu.items():
            if page == "实时预警":
                # 一级按钮：仅负责展开/收起，不切换页面
                if st.button(label,
                             use_container_width=True,
                             type="primary" if st.session_state.alert_sub_expand else "secondary",
                             key="nav_实时预警"):
                    st.session_state.alert_sub_expand = not st.session_state.alert_sub_expand
                    st.rerun()

                # 子按钮（缩进）
                if st.session_state.alert_sub_expand:
                    col_ind, col_sub = st.sidebar.columns([0.1, 0.9])
                    with col_sub:
                        for sub in ["总体分析", "个体分析"]:
                            if st.button(
                                f"✨ {sub}",
                                use_container_width=True,
                                type="primary" if st.session_state.alert_sub_page == sub else "secondary",
                                key=f"nav_{sub}"
                            ):
                                st.session_state.alert_sub_page = sub
                                st.session_state.current_page = sub   # 真正切换页面
                                st.rerun()
            else:
                # 普通一级菜单
                if st.button(label,
                             use_container_width=True,
                             type="primary" if st.session_state.current_page == page else "secondary",
                             key=f"nav_{page}"):
                    st.session_state.current_page = page
                    st.rerun()

        st.markdown("---")
        st.markdown("### ⚙️ 系统", unsafe_allow_html=True)
        if st.button("🔧 设置", use_container_width=True, key="settings"):
            st.session_state.current_page = '设置'
            st.rerun()
        if st.button("💡 建议", use_container_width=True, key="feedback"):
            st.session_state.current_page = '建议反馈'
            st.rerun()


def render_dashboard():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    workers_df, _, _, _, _ = generate_mock_data()

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("⚙️ 今日工程进度", "", "#8b9dc3", "#a0aed0", True),
        ("⚠️ 今日预警个数", "47", "#d4a5a5", "#e3b8b8", False),
        ("🎯  今日干预个数", "34", "#9eb8cc", "#b4c9d9", False),
        ("📊 全局风险指数", "52", "#a8c5b5", "#bcd4c5", False)
    ]

    for col, metric in zip([col1, col2, col3, col4], metrics):
        with col:
            if metric[4]:
                label, value, color1, color2, is_progress = metric
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color1} 0%, {color2} 100%); 
                            padding: 30px 25px; border-radius: 16px; color: white; text-align: center; 
                            min-height: 140px; box-shadow: 0 6px 16px rgba(139, 157, 195, 0.2);
                            transition: transform 0.3s ease, box-shadow 0.3s ease;
                            position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%;
                                background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
                                pointer-events: none;"></div>
                    <div style="font-size: 15px; margin-bottom: 15px; position: relative; z-index: 1; 
                                text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{label}</div>
                    <div style="background: rgba(255,255,255,0.2); height: 32px; border-radius: 10px; 
                                border: 2px solid rgba(255,255,255,0.4); margin: 0 auto; width: 80%; 
                                position: relative; overflow: hidden; z-index: 1;
                                box-shadow: inset 0 2px 4px rgba(0,0,0,0.08);">
                        <div style="position: absolute; left: 0; top: 0; height: 100%; width: 65%; 
                                    background: linear-gradient(90deg, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.8) 100%); 
                                    border-radius: 8px; box-shadow: 0 2px 6px rgba(255,255,255,0.2);"></div>
                    </div>
                    <div style="font-size: 12px; margin-top: 10px; opacity: 0.9; position: relative; z-index: 1; 
                                font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">完成度: 65%</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                label, value, color1, color2, is_progress = metric
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color1} 0%, {color2} 100%); 
                            padding: 30px 25px; border-radius: 16px; color: white; text-align: center; 
                            min-height: 140px; box-shadow: 0 6px 16px {color1}30;
                            transition: transform 0.3s ease, box-shadow 0.3s ease;
                            position: relative; overflow: hidden;">
                    <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%;
                                background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
                                pointer-events: none;"></div>
                    <div style="font-size: 15px; margin-bottom: 15px; position: relative; z-index: 1;
                                text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{label}</div>
                    <div style="font-size: 56px; font-weight: bold; line-height: 1; position: relative; z-index: 1;
                                text-shadow: 0 2px 6px rgba(0,0,0,0.15);">{value}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([7, 3])

    with col_main:
        st.markdown("### 🏗️ 工地3D实时模拟图", unsafe_allow_html=True)

        np.random.seed(42)

        # 扩展工人详细信息
        worker_details = [
            {'name': '张三', 'level': 'L1', 'age': 39, 'id': 'A12011', 'threat': 1, 'pos': (-25, 30, 2),
             'job': '混凝土工', 'status': '浇筑作业中', 'fatigue': 35},
            {'name': '小宇', 'level': 'L2', 'age': 43, 'id': 'A12012', 'threat': 2, 'pos': (15, -20, 3),
             'job': '钢筋工', 'status': '绑扎钢筋', 'fatigue': 62},
            {'name': '李四', 'level': 'L1', 'age': 39, 'id': 'A12013', 'threat': 1, 'pos': (-30, -15, 1),
             'job': '架子工', 'status': '脚手架维护', 'fatigue': 28},
            {'name': '小明', 'level': 'L3', 'age': 45, 'id': 'A12014', 'threat': 3, 'pos': (25, 25, 4),
             'job': '电焊工', 'status': '高空焊接', 'fatigue': 78},
            {'name': '安田', 'level': 'L2', 'age': 43, 'id': 'A12015', 'threat': 2, 'pos': (5, 10, 2),
             'job': '木工', 'status': '模板安装', 'fatigue': 55},
            {'name': '王五', 'level': 'L1', 'age': 38, 'id': 'A12016', 'threat': 1, 'pos': (-10, -25, 1),
             'job': '抹灰工', 'status': '墙面处理', 'fatigue': 42},
            {'name': '小林', 'level': 'L2', 'age': 41, 'id': 'A12017', 'threat': 2, 'pos': (35, -10, 2),
             'job': '电工', 'status': '线路铺设', 'fatigue': 58},
            {'name': '老张', 'level': 'L1', 'age': 52, 'id': 'A12018', 'threat': 1, 'pos': (-35, 15, 1),
             'job': '瓦工', 'status': '砌墙作业', 'fatigue': 45}
        ]

        worker_colors = {
            'L1': '#32CD32',
            'L2': '#FFD700',
            'L3': '#FF4500'
        }

        fig = go.Figure()

        # === 更真实的建筑物配置 - 增加到25栋 ===
        buildings = [
            # 主办公楼群（现代化玻璃幕墙）
            {'x': -30, 'y': 20, 'w': 15, 'h': 20, 'z': 0, 'height': 32, 'type': 'office_tower', 'floors': 10,
             'name': '主办公大楼A座', 'status': '主体完工', 'progress': 85},
            {'x': -15, 'y': 25, 'w': 12, 'h': 16, 'z': 0, 'height': 28, 'type': 'office_tower', 'floors': 9,
             'name': '主办公大楼B座', 'status': '外墙装修中', 'progress': 72},
            {'x': 0, 'y': 22, 'w': 10, 'h': 14, 'z': 0, 'height': 24, 'type': 'office_modern', 'floors': 8,
             'name': '行政办公楼', 'status': '内部装修', 'progress': 68},

            # 高层住宅楼群（带阳台）
            {'x': 25, 'y': 28, 'w': 18, 'h': 14, 'z': 0, 'height': 38, 'type': 'residential_high', 'floors': 12,
             'name': '1号住宅楼', 'status': '封顶', 'progress': 90},
            {'x': 40, 'y': 25, 'w': 16, 'h': 12, 'z': 0, 'height': 35, 'type': 'residential_high', 'floors': 11,
             'name': '2号住宅楼', 'status': '主体施工', 'progress': 75},
            {'x': 38, 'y': 10, 'w': 14, 'h': 13, 'z': 0, 'height': 32, 'type': 'residential_mid', 'floors': 10,
             'name': '3号住宅楼', 'status': '基础完成', 'progress': 45},

            # 工业厂房（大跨度钢结构）
            {'x': -28, 'y': -18, 'w': 16, 'h': 22, 'z': 0, 'height': 18, 'type': 'factory_steel', 'floors': 1,
             'name': '钢结构厂房A', 'status': '钢架安装', 'progress': 60},
            {'x': -10, 'y': -20, 'w': 18, 'h': 24, 'z': 0, 'height': 22, 'type': 'factory_concrete', 'floors': 2,
             'name': '混凝土厂房B', 'status': '屋面施工', 'progress': 55},
            {'x': 8, 'y': -24, 'w': 14, 'h': 18, 'z': 0, 'height': 16, 'type': 'warehouse', 'floors': 1,
             'name': '仓储中心', 'status': '主体完工', 'progress': 88},

            # 商业综合体（复杂立面）
            {'x': 18, 'y': -22, 'w': 22, 'h': 18, 'z': 0, 'height': 28, 'type': 'commercial_complex', 'floors': 7,
             'name': '商业综合体', 'status': '幕墙施工', 'progress': 65},
            {'x': -5, 'y': 5, 'w': 16, 'h': 14, 'z': 0, 'height': 24, 'type': 'shopping_mall', 'floors': 6,
             'name': '购物中心', 'status': '内装进行中', 'progress': 70},

            # 配套设施
            {'x': -40, 'y': 0, 'w': 12, 'h': 10, 'z': 0, 'height': 16, 'type': 'parking', 'floors': 5,
             'name': '立体停车楼', 'status': '结构完成', 'progress': 78},
            {'x': 10, 'y': 2, 'w': 8, 'h': 10, 'z': 0, 'height': 12, 'type': 'utility', 'floors': 3,
             'name': '配电房', 'status': '设备安装', 'progress': 82},
            {'x': -42, 'y': -30, 'w': 10, 'h': 8, 'z': 0, 'height': 8, 'type': 'guard', 'floors': 2,
             'name': '保安室', 'status': '完工', 'progress': 100},

            # 新增建筑
            {'x': 45, 'y': -5, 'w': 12, 'h': 15, 'z': 0, 'height': 20, 'type': 'hotel', 'floors': 6,
             'name': '配套酒店', 'status': '外立面施工', 'progress': 58},
            {'x': -20, 'y': -35, 'w': 14, 'h': 12, 'z': 0, 'height': 10, 'type': 'canteen', 'floors': 2,
             'name': '员工食堂', 'status': '装修收尾', 'progress': 92},
            {'x': 28, 'y': -35, 'w': 10, 'h': 8, 'z': 0, 'height': 14, 'type': 'office_modern', 'floors': 4,
             'name': '项目部办公楼', 'status': '使用中', 'progress': 100},
            {'x': -48, 'y': 20, 'w': 8, 'h': 12, 'z': 0, 'height': 18, 'type': 'residential_mid', 'floors': 6,
             'name': '人才公寓', 'status': '主体施工', 'progress': 52},
            {'x': 48, 'y': 38, 'w': 12, 'h': 10, 'z': 0, 'height': 15, 'type': 'education', 'floors': 4,
             'name': '幼儿园', 'status': '基础施工', 'progress': 35},
            {'x': -8, 'y': 38, 'w': 14, 'h': 11, 'z': 0, 'height': 12, 'type': 'sports', 'floors': 3,
             'name': '健身中心', 'status': '结构完成', 'progress': 68},
            {'x': 12, 'y': 38, 'w': 10, 'h': 9, 'z': 0, 'height': 8, 'type': 'community', 'floors': 2,
             'name': '社区服务中心', 'status': '装修中', 'progress': 75},
            {'x': -45, 'y': -12, 'w': 9, 'h': 11, 'z': 0, 'height': 11, 'type': 'medical', 'floors': 3,
             'name': '医疗站', 'status': '设备安装', 'progress': 80},
            {'x': 50, 'y': 15, 'w': 8, 'h': 8, 'z': 0, 'height': 6, 'type': 'substation', 'floors': 1,
             'name': '变电站', 'status': '调试中', 'progress': 95},
            {'x': 5, 'y': -38, 'w': 16, 'h': 8, 'z': 0, 'height': 5, 'type': 'material_storage', 'floors': 1,
             'name': '材料堆场', 'status': '使用中', 'progress': 100},
            {'x': -25, 'y': 38, 'w': 11, 'h': 9, 'z': 0, 'height': 9, 'type': 'laboratory', 'floors': 2,
             'name': '检测实验室', 'status': '设备进场', 'progress': 72}
        ]

        # 更丰富的建筑类型配色和材质
        building_styles = {
            'office_tower': {'color': 'rgba(70, 130, 180, 0.6)', 'edge': 'rgba(50, 100, 150, 0.9)',
                             'window': 'rgba(135, 206, 250, 0.9)'},
            'office_modern': {'color': 'rgba(100, 149, 237, 0.6)', 'edge': 'rgba(70, 119, 207, 0.9)',
                              'window': 'rgba(176, 224, 230, 0.9)'},
            'residential_high': {'color': 'rgba(188, 143, 143, 0.6)', 'edge': 'rgba(158, 113, 113, 0.9)',
                                 'window': 'rgba(255, 218, 185, 0.8)'},
            'residential_mid': {'color': 'rgba(205, 170, 125, 0.6)', 'edge': 'rgba(175, 140, 95, 0.9)',
                                'window': 'rgba(255, 235, 205, 0.8)'},
            'factory_steel': {'color': 'rgba(169, 169, 169, 0.6)', 'edge': 'rgba(105, 105, 105, 0.9)',
                              'window': 'rgba(192, 192, 192, 0.7)'},
            'factory_concrete': {'color': 'rgba(128, 128, 128, 0.6)', 'edge': 'rgba(88, 88, 88, 0.9)',
                                 'window': 'rgba(160, 160, 160, 0.7)'},
            'warehouse': {'color': 'rgba(144, 144, 144, 0.6)', 'edge': 'rgba(96, 96, 96, 0.9)',
                          'window': 'rgba(176, 176, 176, 0.7)'},
            'commercial_complex': {'color': 'rgba(210, 180, 140, 0.6)', 'edge': 'rgba(180, 150, 110, 0.9)',
                                   'window': 'rgba(255, 228, 181, 0.9)'},
            'shopping_mall': {'color': 'rgba(222, 184, 135, 0.6)', 'edge': 'rgba(192, 154, 105, 0.9)',
                              'window': 'rgba(255, 239, 213, 0.9)'},
            'parking': {'color': 'rgba(112, 128, 144, 0.7)', 'edge': 'rgba(82, 98, 114, 0.9)',
                        'window': 'rgba(176, 196, 222, 0.6)'},
            'utility': {'color': 'rgba(119, 136, 153, 0.7)', 'edge': 'rgba(89, 106, 123, 0.9)',
                        'window': 'rgba(192, 192, 192, 0.6)'},
            'guard': {'color': 'rgba(160, 82, 45, 0.7)', 'edge': 'rgba(130, 52, 15, 0.9)',
                      'window': 'rgba(210, 180, 140, 0.8)'},
            'hotel': {'color': 'rgba(218, 165, 32, 0.6)', 'edge': 'rgba(188, 135, 2, 0.9)',
                      'window': 'rgba(255, 215, 0, 0.8)'},
            'canteen': {'color': 'rgba(244, 164, 96, 0.6)', 'edge': 'rgba(214, 134, 66, 0.9)',
                        'window': 'rgba(255, 218, 185, 0.8)'},
            'education': {'color': 'rgba(255, 182, 193, 0.6)', 'edge': 'rgba(225, 152, 163, 0.9)',
                          'window': 'rgba(255, 240, 245, 0.8)'},
            'sports': {'color': 'rgba(60, 179, 113, 0.6)', 'edge': 'rgba(30, 149, 83, 0.9)',
                       'window': 'rgba(144, 238, 144, 0.7)'},
            'community': {'color': 'rgba(147, 112, 219, 0.6)', 'edge': 'rgba(117, 82, 189, 0.9)',
                          'window': 'rgba(221, 160, 221, 0.8)'},
            'medical': {'color': 'rgba(255, 99, 71, 0.6)', 'edge': 'rgba(225, 69, 41, 0.9)',
                        'window': 'rgba(255, 160, 122, 0.8)'},
            'substation': {'color': 'rgba(47, 79, 79, 0.7)', 'edge': 'rgba(17, 49, 49, 0.9)',
                           'window': 'rgba(112, 128, 144, 0.6)'},
            'material_storage': {'color': 'rgba(205, 133, 63, 0.6)', 'edge': 'rgba(175, 103, 33, 0.9)',
                                 'window': 'rgba(222, 184, 135, 0.6)'},
            'laboratory': {'color': 'rgba(95, 158, 160, 0.6)', 'edge': 'rgba(65, 128, 130, 0.9)',
                           'window': 'rgba(175, 238, 238, 0.8)'}
        }

        # 绘制详细建筑物
        for building in buildings:
            x, y, w, h, z, height = building['x'], building['y'], building['w'], building['h'], building['z'], building[
                'height']
            building_type = building['type']
            floors = building['floors']
            name = building['name']
            status = building['status']
            progress = building['progress']

            style = building_styles[building_type]

            # 建筑主体顶点
            vertices_x = [x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2, x + w / 2, x + w / 2, x - w / 2]
            vertices_y = [y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2, y - h / 2, y + h / 2, y + h / 2]
            vertices_z = [z, z, z, z, z + height, z + height, z + height, z + height]

            # 建筑主体（带悬停信息）
            fig.add_trace(go.Mesh3d(
                x=vertices_x, y=vertices_y, z=vertices_z,
                i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                color=style['color'],
                opacity=0.75,
                showlegend=False,
                flatshading=False,
                lighting=dict(ambient=0.5, diffuse=0.9, specular=0.6, roughness=0.4),
                lightposition=dict(x=100, y=100, z=300),
                hovertemplate=f"<b>🏢 {name}</b><br>" +
                              f"类型: {building_type.replace('_', ' ').title()}<br>" +
                              f"楼层: {floors}层<br>" +
                              f"高度: {height}m<br>" +
                              f"状态: {status}<br>" +
                              f"进度: {progress}%<br>" +
                              f"占地: {w}m × {h}m<br>" +
                              "<extra></extra>"
            ))

            # 建筑边框（加粗）
            edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]
            for edge in edges:
                fig.add_trace(go.Scatter3d(
                    x=[vertices_x[edge[0]], vertices_x[edge[1]]],
                    y=[vertices_y[edge[0]], vertices_y[edge[1]]],
                    z=[vertices_z[edge[0]], vertices_z[edge[1]]],
                    mode='lines',
                    line=dict(color=style['edge'], width=3),
                    showlegend=False,
                    hoverinfo='skip'
                ))

            # 楼层分隔线（更明显）
            floor_height = height / floors
            for floor in range(1, floors):
                floor_z = z + floor * floor_height
                fig.add_trace(go.Scatter3d(
                    x=[x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2],
                    y=[y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2],
                    z=[floor_z, floor_z, floor_z, floor_z, floor_z],
                    mode='lines',
                    line=dict(color='rgba(255, 255, 255, 0.4)', width=1.5),
                    showlegend=False,
                    hoverinfo='skip'
                ))

            # 窗户（更密集更真实）
            window_spacing_x = max(2.5, w / 6)
            window_spacing_y = max(2.5, h / 6)

            for floor in range(floors):
                floor_z = z + (floor + 0.5) * floor_height

                # 前后墙窗户
                for i in range(int(w / window_spacing_x)):
                    wx = x - w / 2 + (i + 0.5) * window_spacing_x
                    # 前墙
                    fig.add_trace(go.Scatter3d(
                        x=[wx], y=[y - h / 2], z=[floor_z],
                        mode='markers',
                        marker=dict(size=4, color=style['window'], symbol='square'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    # 后墙
                    fig.add_trace(go.Scatter3d(
                        x=[wx], y=[y + h / 2], z=[floor_z],
                        mode='markers',
                        marker=dict(size=4, color=style['window'], symbol='square'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                # 左右墙窗户
                for j in range(int(h / window_spacing_y)):
                    wy = y - h / 2 + (j + 0.5) * window_spacing_y
                    # 左墙
                    fig.add_trace(go.Scatter3d(
                        x=[x - w / 2], y=[wy], z=[floor_z],
                        mode='markers',
                        marker=dict(size=4, color=style['window'], symbol='square'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
                    # 右墙
                    fig.add_trace(go.Scatter3d(
                        x=[x + w / 2], y=[wy], z=[floor_z],
                        mode='markers',
                        marker=dict(size=4, color=style['window'], symbol='square'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

        # 添加更多脚手架
        scaffolds = [
            {'x': -30, 'y': 20, 'w': 15, 'h': 20, 'height': 32, 'name': '主办公楼A座脚手架'},
            {'x': 25, 'y': 28, 'w': 18, 'h': 14, 'height': 38, 'name': '1号住宅楼脚手架'},
            {'x': 18, 'y': -22, 'w': 22, 'h': 18, 'height': 28, 'name': '商业综合体脚手架'},
        ]

        for scaffold in scaffolds:
            x, y, w, h, height, name = scaffold['x'], scaffold['y'], scaffold['w'], scaffold['h'], scaffold['height'], \
            scaffold['name']

            # 垂直杆（带悬停信息）
            for i in range(6):
                for j in range(6):
                    sx = x - w / 2 + i * w / 5
                    sy = y - h / 2 + j * h / 5
                    fig.add_trace(go.Scatter3d(
                        x=[sx, sx], y=[sy, sy], z=[0, height],
                        mode='lines',
                        line=dict(color='rgba(255, 165, 0, 0.6)', width=2.5),
                        showlegend=False,
                        hovertemplate=f"<b>⚙️ {name}</b><br>" +
                                      f"类型: 外挂脚手架<br>" +
                                      f"高度: {height}m<br>" +
                                      f"状态: 施工中<br>" +
                                      "<extra></extra>"
                    ))

            # 水平杆
            for level in range(0, int(height), 4):
                fig.add_trace(go.Scatter3d(
                    x=[x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2],
                    y=[y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2],
                    z=[level, level, level, level, level],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.5)', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))

        # 塔吊（更详细，带悬停信息）
        cranes = [
            {'x': 25, 'y': -10, 'height': 40, 'arm_length': 25, 'name': '1号塔吊', 'model': 'QTZ80', 'load': '8吨'},
            {'x': -35, 'y': 15, 'height': 38, 'arm_length': 22, 'name': '2号塔吊', 'model': 'QTZ63', 'load': '6吨'},
        ]

        for crane in cranes:
            cx, cy, ch, arm_len = crane['x'], crane['y'], crane['height'], crane['arm_length']

            # 塔身
            fig.add_trace(go.Scatter3d(
                x=[cx, cx], y=[cy, cy], z=[0, ch],
                mode='lines',
                line=dict(color='rgba(255, 215, 0, 0.95)', width=10),
                showlegend=False,
                hovertemplate=f"<b>🏗️ {crane['name']}</b><br>" +
                              f"型号: {crane['model']}<br>" +
                              f"额定载重: {crane['load']}<br>" +
                              f"高度: {ch}m<br>" +
                              f"臂长: {arm_len}m<br>" +
                              f"状态: 运行中<br>" +
                              "<extra></extra>"
            ))

            # 主吊臂
            fig.add_trace(go.Scatter3d(
                x=[cx - arm_len, cx + arm_len],
                y=[cy, cy],
                z=[ch, ch],
                mode='lines',
                line=dict(color='rgba(255, 215, 0, 0.95)', width=7),
                showlegend=False,
                hoverinfo='skip'
            ))

            # 平衡臂
            fig.add_trace(go.Scatter3d(
                x=[cx, cx - arm_len * 0.6],
                y=[cy, cy],
                z=[ch, ch],
                mode='lines',
                line=dict(color='rgba(255, 215, 0, 0.95)', width=6),
                showlegend=False,
                hoverinfo='skip'
            ))

            # 吊钩（动画效果）
            hook_x = cx + arm_len * 0.4
            hook_z = ch - 15
            fig.add_trace(go.Scatter3d(
                x=[hook_x, hook_x],
                y=[cy, cy],
                z=[ch, hook_z],
                mode='lines',
                line=dict(color='rgba(50, 50, 50, 0.8)', width=2),
                showlegend=False,
                hoverinfo='skip'
            ))
            fig.add_trace(go.Scatter3d(
                x=[hook_x],
                y=[cy],
                z=[hook_z],
                mode='markers',
                marker=dict(size=6, color='#FF4500', symbol='diamond'),
                showlegend=False,
                hovertemplate="🪝 吊钩<br>状态: 待命<br><extra></extra>"
            ))

        # 施工围栏（带大门）
        fence_points = [
            [-52, -42], [52, -42], [52, 45], [-52, 45], [-52, -42]
        ]
        for i in range(len(fence_points) - 1):
            # 跳过大门位置
            if i == 0 and abs(fence_points[i][0]) < 5:
                continue
            fig.add_trace(go.Scatter3d(
                x=[fence_points[i][0], fence_points[i + 1][0]],
                y=[fence_points[i][1], fence_points[i + 1][1]],
                z=[0, 0],
                mode='lines',
                line=dict(color='rgba(255, 0, 0, 0.6)', width=4),
                showlegend=False,
                hovertemplate="<b>🚧 施工围栏</b><br>高度: 2m<br>材质: 彩钢板<br><extra></extra>"
            ))

        # 添加大门
        gate_x = [-5, 5]
        gate_y = [-42, -42]
        fig.add_trace(go.Scatter3d(
            x=gate_x, y=gate_y, z=[0, 0],
            mode='lines',
            line=dict(color='rgba(0, 128, 0, 0.8)', width=6),
            showlegend=False,
            hovertemplate="<b>🚪 工地大门</b><br>宽度: 10m<br>状态: 开启<br><extra></extra>"
        ))

        # 绘制3D工人模型（增强版，带详细信息）
        if st.session_state.show_workers:
            for worker in worker_details:
                color = worker_colors[worker['level']]
                x, y, z = worker['pos']

                # 人体比例
                head_radius = 0.4
                body_height = 1.5
                body_width = 0.6
                leg_height = 1.2

                # 头部（球体）
                theta = np.linspace(0, 2 * np.pi, 10)
                phi = np.linspace(0, np.pi, 10)
                head_x = x + head_radius * np.outer(np.cos(theta), np.sin(phi))
                head_y = y + head_radius * np.outer(np.sin(theta), np.sin(phi))
                head_z = z + body_height + leg_height + head_radius + head_radius * np.outer(np.ones(10), np.cos(phi))

                fig.add_trace(go.Surface(
                    x=head_x, y=head_y, z=head_z,
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    showlegend=False,
                    opacity=0.9,
                    hovertemplate=f"<b>👤 {worker['name']}</b><br>" +
                                  f"工号: {worker['id']}<br>" +
                                  f"年龄: {worker['age']}岁<br>" +
                                  f"等级: {worker['level']}<br>" +
                                  f"职位: {worker['job']}<br>" +
                                  f"当前状态: {worker['status']}<br>" +
                                  f"疲劳度: {worker['fatigue']}%<br>" +
                                  f"威胁级别: {worker['threat']}级<br>" +
                                  "<extra></extra>"
                ))

                # 身体
                body_vertices_x = [
                    x - body_width / 2, x + body_width / 2, x + body_width / 2, x - body_width / 2,
                    x - body_width / 2, x + body_width / 2, x + body_width / 2, x - body_width / 2
                ]
                body_vertices_y = [
                    y - body_width / 2, y - body_width / 2, y + body_width / 2, y + body_width / 2,
                    y - body_width / 2, y - body_width / 2, y + body_width / 2, y + body_width / 2
                ]
                body_vertices_z = [
                    z + leg_height, z + leg_height, z + leg_height, z + leg_height,
                    z + leg_height + body_height, z + leg_height + body_height,
                    z + leg_height + body_height, z + leg_height + body_height
                ]

                fig.add_trace(go.Mesh3d(
                    x=body_vertices_x, y=body_vertices_y, z=body_vertices_z,
                    i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                    k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                    color=color,
                    opacity=0.85,
                    showlegend=False,
                    hoverinfo='skip'
                ))

                # 腿部
                for leg_offset in [-body_width / 3, body_width / 3]:
                    fig.add_trace(go.Scatter3d(
                        x=[x + leg_offset, x + leg_offset],
                        y=[y, y],
                        z=[z, z + leg_height],
                        mode='lines',
                        line=dict(color=color, width=7),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                # 手臂
                arm_z = z + leg_height + body_height * 0.7
                for arm_offset in [-body_width / 2 - 0.2, body_width / 2 + 0.2]:
                    fig.add_trace(go.Scatter3d(
                        x=[x, x + arm_offset],
                        y=[y, y],
                        z=[arm_z, arm_z - 0.3],
                        mode='lines',
                        line=dict(color=color, width=6),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                # 安全帽
                hat_z = z + body_height + leg_height + head_radius * 2
                fig.add_trace(go.Scatter3d(
                    x=[x], y=[y], z=[hat_z + 0.3],
                    mode='markers',
                    marker=dict(size=9, color='#FFD700', symbol='diamond'),
                    showlegend=False,
                    hoverinfo='skip'
                ))

                # 工人标签（带背景）
                fig.add_trace(go.Scatter3d(
                    x=[x], y=[y], z=[hat_z + 0.8],
                    mode='text',
                    text=[worker['name']],
                    textposition='top center',
                    textfont=dict(size=11, color='white', family='Arial Black'),
                    showlegend=False,
                    hoverinfo='skip'
                ))

        # 施工设备（增强版，带详细信息）
        equipments = [
            {'x': -38, 'y': -28, 'z': 0, 'type': 'excavator', 'name': '挖掘机CAT320', 'status': '作业中',
             'operator': '李师傅'},
            {'x': 8, 'y': -32, 'z': 0, 'type': 'mixer', 'name': '混凝土搅拌车', 'status': '待料中',
             'operator': '王师傅'},
            {'x': 38, 'y': 12, 'z': 0, 'type': 'truck', 'name': '运输卡车', 'status': '装载中', 'operator': '张师傅'},
            {'x': -20, 'y': -38, 'z': 0, 'type': 'loader', 'name': '装载机', 'status': '运行中', 'operator': '赵师傅'},
            {'x': 42, 'y': -28, 'z': 0, 'type': 'pump', 'name': '混凝土泵车', 'status': '泵送中', 'operator': '刘师傅'},
        ]

        equipment_colors = {
            'excavator': 'rgba(255, 140, 0, 0.8)',
            'mixer': 'rgba(70, 130, 180, 0.8)',
            'truck': 'rgba(34, 139, 34, 0.8)',
            'loader': 'rgba(218, 165, 32, 0.8)',
            'pump': 'rgba(220, 20, 60, 0.8)'
        }

        for eq in equipments:
            eq_color = equipment_colors[eq['type']]

            fig.add_trace(go.Mesh3d(
                x=[eq['x'] - 2, eq['x'] + 2, eq['x'] + 2, eq['x'] - 2, eq['x'] - 2, eq['x'] + 2, eq['x'] + 2,
                   eq['x'] - 2],
                y=[eq['y'] - 1.5, eq['y'] - 1.5, eq['y'] + 1.5, eq['y'] + 1.5, eq['y'] - 1.5, eq['y'] - 1.5,
                   eq['y'] + 1.5, eq['y'] + 1.5],
                z=[eq['z'], eq['z'], eq['z'], eq['z'], eq['z'] + 2.5, eq['z'] + 2.5, eq['z'] + 2.5, eq['z'] + 2.5],
                i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                color=eq_color,
                opacity=0.85,
                showlegend=False,
                hovertemplate=f"<b>🚜 {eq['name']}</b><br>" +
                              f"类型: {eq['type'].title()}<br>" +
                              f"状态: {eq['status']}<br>" +
                              f"操作员: {eq['operator']}<br>" +
                              f"位置: ({eq['x']:.1f}, {eq['y']:.1f})<br>" +
                              "<extra></extra>"
            ))

        # 添加道路网络
        roads = [
            {'start': [-52, 0], 'end': [52, 0], 'width': 6, 'name': '主干道'},
            {'start': [0, -42], 'end': [0, 45], 'width': 5, 'name': '次干道'},
            {'start': [-25, -42], 'end': [-25, 45], 'width': 4, 'name': '施工通道1'},
            {'start': [25, -42], 'end': [25, 45], 'width': 4, 'name': '施工通道2'},
        ]

        for road in roads:
            fig.add_trace(go.Scatter3d(
                x=[road['start'][0], road['end'][0]],
                y=[road['start'][1], road['end'][1]],
                z=[0.05, 0.05],
                mode='lines',
                line=dict(color='rgba(64, 64, 64, 0.6)', width=road['width']),
                showlegend=False,
                hovertemplate=f"<b>🛣️ {road['name']}</b><br>宽度: {road['width']}m<br><extra></extra>"
            ))

        # 相机设置
        zoom = st.session_state.camera_zoom
        rotation = st.session_state.camera_rotation
        rotation_rad = np.radians(rotation)

        eye_x = 2.0 * zoom * np.cos(rotation_rad)
        eye_y = 2.0 * zoom * np.sin(rotation_rad)

        fig.update_layout(
            scene=dict(
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.3)',
                    showbackground=True,
                    backgroundcolor='rgba(240, 248, 255, 0.3)',
                    title='',
                    showticklabels=False,
                    range=[-60, 60]
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.3)',
                    showbackground=True,
                    backgroundcolor='rgba(240, 248, 255, 0.3)',
                    title='',
                    showticklabels=False,
                    range=[-50, 50]
                ),
                zaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(200,200,200,0.3)',
                    showbackground=True,
                    backgroundcolor='rgba(240, 248, 255, 0.3)',
                    title='',
                    showticklabels=False,
                    range=[0, 50]
                ),
                bgcolor='rgba(20, 40, 80, 0.95)',
                camera=dict(
                    eye=dict(x=eye_x, y=eye_y, z=1.3 * zoom),
                    center=dict(x=0, y=0, z=0)
                ),
                aspectmode='cube'
            ),
            height=550,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor='rgba(20, 40, 80, 0.98)',
            showlegend=False,
            hovermode='closest'
        )

        st.plotly_chart(fig, use_container_width=True, key="3d_view", config={
            'modeBarButtonsToRemove': ['zoom3d', 'pan3d', 'orbitRotation', 'tableRotation',
                                       'resetCameraDefault3d', 'resetCameraLastSave3d'],
            'displaylogo': False
        })

        # 更真实的建筑物配置 - 增加更多细节
        buildings = [
            # 主楼群
            {'x': -30, 'y': 20, 'w': 15, 'h': 20, 'z': 0, 'height': 28, 'type': 'office', 'floors': 8},
            {'x': -15, 'y': 25, 'w': 12, 'h': 16, 'z': 0, 'height': 24, 'type': 'office', 'floors': 7},
            {'x': 0, 'y': 22, 'w': 10, 'h': 14, 'z': 0, 'height': 20, 'type': 'office', 'floors': 6},

            # 住宅楼群
            {'x': 25, 'y': 28, 'w': 18, 'h': 14, 'z': 0, 'height': 32, 'type': 'residential', 'floors': 10},
            {'x': 40, 'y': 25, 'w': 16, 'h': 12, 'z': 0, 'height': 28, 'type': 'residential', 'floors': 9},

            # 工业厂房
            {'x': -28, 'y': -18, 'w': 14, 'h': 18, 'z': 0, 'height': 18, 'type': 'factory', 'floors': 1},
            {'x': -10, 'y': -20, 'w': 16, 'h': 20, 'z': 0, 'height': 22, 'type': 'factory', 'floors': 1},

            # 商业建筑
            {'x': 18, 'y': -22, 'w': 20, 'h': 16, 'z': 0, 'height': 26, 'type': 'commercial', 'floors': 6},
            {'x': 38, 'y': -18, 'w': 14, 'h': 14, 'z': 0, 'height': 22, 'type': 'commercial', 'floors': 5},

            # 低层配套建筑
            {'x': -5, 'y': 0, 'w': 10, 'h': 12, 'z': 0, 'height': 14, 'type': 'support', 'floors': 4},
            {'x': 10, 'y': 2, 'w': 8, 'h': 10, 'z': 0, 'height': 12, 'type': 'support', 'floors': 3},
            {'x': -40, 'y': 0, 'w': 12, 'h': 10, 'z': 0, 'height': 16, 'type': 'support', 'floors': 4},
        ]

        # 建筑类型配色方案
        building_colors = {
            'office': 'rgba(70, 130, 180, 0.5)',  # 钢蓝色 - 办公楼
            'residential': 'rgba(188, 143, 143, 0.5)',  # 玫瑰褐 - 住宅
            'factory': 'rgba(169, 169, 169, 0.5)',  # 灰色 - 工厂
            'commercial': 'rgba(210, 180, 140, 0.5)',  # 棕褐色 - 商业
            'support': 'rgba(144, 238, 144, 0.5)'  # 浅绿色 - 配套
        }

        # 绘制更详细的建筑物
        for building in buildings:
            x, y, w, h, z, height = building['x'], building['y'], building['w'], building['h'], building['z'], building[
                'height']
            building_type = building['type']
            floors = building['floors']

            # 主体建筑
            vertices_x = [x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2, x + w / 2, x + w / 2, x - w / 2]
            vertices_y = [y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2, y - h / 2, y + h / 2, y + h / 2]
            vertices_z = [z, z, z, z, z + height, z + height, z + height, z + height]

            # 建筑主体
            fig.add_trace(go.Mesh3d(
                x=vertices_x,
                y=vertices_y,
                z=vertices_z,
                i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                color=building_colors[building_type],
                opacity=0.7,
                showlegend=False,
                hoverinfo='skip',
                flatshading=False,
                lighting=dict(ambient=0.4, diffuse=0.9, specular=0.5, roughness=0.5),
                lightposition=dict(x=100, y=100, z=300)
            ))

            # 建筑边框
            edges = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]
            for edge in edges:
                fig.add_trace(go.Scatter3d(
                    x=[vertices_x[edge[0]], vertices_x[edge[1]]],
                    y=[vertices_y[edge[0]], vertices_y[edge[1]]],
                    z=[vertices_z[edge[0]], vertices_z[edge[1]]],
                    mode='lines',
                    line=dict(color='rgba(50, 50, 50, 0.8)', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))

            # 添加楼层线条（窗户效果）
            floor_height = height / floors
            for floor in range(1, floors):
                floor_z = z + floor * floor_height
                # 横向楼层线
                fig.add_trace(go.Scatter3d(
                    x=[x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2],
                    y=[y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2],
                    z=[floor_z, floor_z, floor_z, floor_z, floor_z],
                    mode='lines',
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=1),
                    showlegend=False,
                    hoverinfo='skip'
                ))

            # 添加窗户（简化表示）
            window_spacing = 3
            for floor in range(floors):
                floor_z = z + (floor + 0.5) * floor_height
                # 前墙窗户
                for i in range(int(w / window_spacing)):
                    wx = x - w / 2 + (i + 0.5) * window_spacing
                    fig.add_trace(go.Scatter3d(
                        x=[wx],
                        y=[y - h / 2],
                        z=[floor_z],
                        mode='markers',
                        marker=dict(size=3, color='rgba(135, 206, 250, 0.8)', symbol='square'),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

        # 添加施工脚手架
        scaffolds = [
            {'x': -30, 'y': 20, 'w': 15, 'h': 20, 'height': 28},
            {'x': 25, 'y': 28, 'w': 18, 'h': 14, 'height': 32},
        ]

        for scaffold in scaffolds:
            x, y, w, h, height = scaffold['x'], scaffold['y'], scaffold['w'], scaffold['h'], scaffold['height']
            # 垂直杆
            for i in range(5):
                for j in range(5):
                    sx = x - w / 2 + i * w / 4
                    sy = y - h / 2 + j * h / 4
                    fig.add_trace(go.Scatter3d(
                        x=[sx, sx],
                        y=[sy, sy],
                        z=[0, height],
                        mode='lines',
                        line=dict(color='rgba(255, 165, 0, 0.5)', width=2),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

            # 水平杆
            for level in range(0, int(height), 4):
                fig.add_trace(go.Scatter3d(
                    x=[x - w / 2, x + w / 2, x + w / 2, x - w / 2, x - w / 2],
                    y=[y - h / 2, y - h / 2, y + h / 2, y + h / 2, y - h / 2],
                    z=[level, level, level, level, level],
                    mode='lines',
                    line=dict(color='rgba(255, 165, 0, 0.4)', width=1.5),
                    showlegend=False,
                    hoverinfo='skip'
                ))

        # 添加塔吊（更详细）
        crane_x, crane_y = 25, -10
        # 塔身
        fig.add_trace(go.Scatter3d(
            x=[crane_x, crane_x],
            y=[crane_y, crane_y],
            z=[0, 35],
            mode='lines',
            line=dict(color='rgba(255, 215, 0, 0.9)', width=8),
            showlegend=False,
            hoverinfo='skip'
        ))
        # 吊臂
        fig.add_trace(go.Scatter3d(
            x=[crane_x - 20, crane_x + 20],
            y=[crane_y, crane_y],
            z=[35, 35],
            mode='lines',
            line=dict(color='rgba(255, 215, 0, 0.9)', width=6),
            showlegend=False,
            hoverinfo='skip'
        ))
        # 平衡臂
        fig.add_trace(go.Scatter3d(
            x=[crane_x, crane_x - 15],
            y=[crane_y, crane_y],
            z=[35, 35],
            mode='lines',
            line=dict(color='rgba(255, 215, 0, 0.9)', width=5),
            showlegend=False,
            hoverinfo='skip'
        ))

        # 添加施工围栏
        fence_points = [
            [-45, -35], [45, -35], [45, 40], [-45, 40], [-45, -35]
        ]
        for i in range(len(fence_points) - 1):
            fig.add_trace(go.Scatter3d(
                x=[fence_points[i][0], fence_points[i + 1][0]],
                y=[fence_points[i][1], fence_points[i + 1][1]],
                z=[0, 0],
                mode='lines',
                line=dict(color='rgba(255, 0, 0, 0.5)', width=3),
                showlegend=False,
                hoverinfo='skip'
            ))

        # 绘制真实的3D人物模型
        if st.session_state.show_workers:
            for worker in worker_details:
                color = worker_colors[worker['level']]
                x, y, z = worker['pos']

                # 人体比例
                head_radius = 0.4
                body_height = 1.5
                body_width = 0.6
                leg_height = 1.2
                arm_length = 1.0

                # 头部（球体）
                theta = np.linspace(0, 2 * np.pi, 10)
                phi = np.linspace(0, np.pi, 10)
                head_x = x + head_radius * np.outer(np.cos(theta), np.sin(phi))
                head_y = y + head_radius * np.outer(np.sin(theta), np.sin(phi))
                head_z = z + body_height + leg_height + head_radius + head_radius * np.outer(np.ones(10), np.cos(phi))

                fig.add_trace(go.Surface(
                    x=head_x, y=head_y, z=head_z,
                    colorscale=[[0, color], [1, color]],
                    showscale=False,
                    showlegend=False,
                    hoverinfo='skip',
                    opacity=0.9
                ))

                # 身体（长方体简化）
                body_vertices_x = [
                    x - body_width / 2, x + body_width / 2, x + body_width / 2, x - body_width / 2,
                    x - body_width / 2, x + body_width / 2, x + body_width / 2, x - body_width / 2
                ]
                body_vertices_y = [
                    y - body_width / 2, y - body_width / 2, y + body_width / 2, y + body_width / 2,
                    y - body_width / 2, y - body_width / 2, y + body_width / 2, y + body_width / 2
                ]
                body_vertices_z = [
                    z + leg_height, z + leg_height, z + leg_height, z + leg_height,
                    z + leg_height + body_height, z + leg_height + body_height,
                    z + leg_height + body_height, z + leg_height + body_height
                ]

                fig.add_trace(go.Mesh3d(
                    x=body_vertices_x, y=body_vertices_y, z=body_vertices_z,
                    i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                    j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                    k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                    color=color,
                    opacity=0.85,
                    showlegend=False,
                    hoverinfo='skip'
                ))

                # 腿部（两条线）
                for leg_offset in [-body_width / 3, body_width / 3]:
                    fig.add_trace(go.Scatter3d(
                        x=[x + leg_offset, x + leg_offset],
                        y=[y, y],
                        z=[z, z + leg_height],
                        mode='lines',
                        line=dict(color=color, width=6),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                # 手臂（两条线）
                arm_z = z + leg_height + body_height * 0.7
                for arm_offset in [-body_width / 2 - 0.2, body_width / 2 + 0.2]:
                    fig.add_trace(go.Scatter3d(
                        x=[x, x + arm_offset],
                        y=[y, y],
                        z=[arm_z, arm_z - 0.3],
                        mode='lines',
                        line=dict(color=color, width=5),
                        showlegend=False,
                        hoverinfo='skip'
                    ))

                # 安全帽（圆锥体顶部标识）
                hat_z = z + body_height + leg_height + head_radius * 2
                fig.add_trace(go.Scatter3d(
                    x=[x],
                    y=[y],
                    z=[hat_z + 0.3],
                    mode='markers',
                    marker=dict(size=8, color='#FFD700', symbol='diamond'),
                    showlegend=False,
                    hoverinfo='skip'
                ))

                # 工人标签
                fig.add_trace(go.Scatter3d(
                    x=[x],
                    y=[y],
                    z=[hat_z + 0.8],
                    mode='text',
                    text=[worker['name']],
                    textposition='top center',
                    textfont=dict(size=10, color='white', family='Arial Black'),
                    showlegend=False,
                    hovertemplate=f"<b>{worker['name']}</b><br>" +
                                  f"年龄: {worker['age']}岁<br>" +
                                  f"等级: {worker['level']}<br>" +
                                  f"工号: {worker['id']}<br>" +
                                  f"威胁状态: {worker['threat']}级<br>" +
                                  "<extra></extra>"
                ))

        # 添加施工设备（挖掘机、混凝土搅拌车等的简化表示）
        equipments = [
            {'x': -35, 'y': -25, 'z': 0, 'type': 'excavator'},
            {'x': 5, 'y': -30, 'z': 0, 'type': 'mixer'},
            {'x': 35, 'y': 10, 'z': 0, 'type': 'truck'}
        ]

        for eq in equipments:
            # 简化的设备方块表示
            fig.add_trace(go.Mesh3d(
                x=[eq['x'] - 1.5, eq['x'] + 1.5, eq['x'] + 1.5, eq['x'] - 1.5, eq['x'] - 1.5, eq['x'] + 1.5,
                   eq['x'] + 1.5, eq['x'] - 1.5],
                y=[eq['y'] - 1, eq['y'] - 1, eq['y'] + 1, eq['y'] + 1, eq['y'] - 1, eq['y'] - 1, eq['y'] + 1,
                   eq['y'] + 1],
                z=[eq['z'], eq['z'], eq['z'], eq['z'], eq['z'] + 2, eq['z'] + 2, eq['z'] + 2, eq['z'] + 2],
                i=[0, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
                j=[1, 2, 3, 4, 5, 6, 7, 4, 0, 1, 6, 3],
                k=[2, 3, 4, 7, 6, 7, 4, 5, 1, 5, 7, 6],
                color='rgba(255, 140, 0, 0.7)',
                opacity=0.8,
                showlegend=False,
                hoverinfo='skip'
            ))

        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(248,250,252,0.97) 100%); 
                    padding: 25px 30px; border-radius: 16px; margin-top: 20px;
                    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.9);
                    position: relative; overflow: hidden;
                    min-height: 200px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;'>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                        background: linear-gradient(90deg, rgba(212,165,165,0.03) 0%, rgba(227,200,153,0.03) 50%, rgba(168,197,181,0.03) 100%);
                        pointer-events: none;"></div>
            <div style="position: relative; z-index: 1;">
                <div style='margin: 15px 0; display: flex; align-items: center;'>
                    <span style='background: linear-gradient(135deg, #d4a5a5 0%, #c49090 100%); 
                                 color: white; padding: 6px 18px; border-radius: 10px; 
                                 font-weight: 600; display: inline-flex; align-items: center;
                                 box-shadow: 0 3px 8px rgba(212, 165, 165, 0.3);
                                 min-width: 130px; justify-content: center;
                                 font-size: 15px;'>
                        🔴 L3 高危
                    </span>
                    <span style='color: #5a6c7d; margin-left: 20px; font-size: 15px;'>近期违规+注意力低下<70%</span>
                </div>
                <div style='margin: 15px 0; display: flex; align-items: center;'>
                    <span style='background: linear-gradient(135deg, #e3c899 0%, #d4bb88 100%); 
                                 color: white; padding: 6px 18px; border-radius: 10px; 
                                 font-weight: 600; display: inline-flex; align-items: center;
                                 box-shadow: 0 3px 8px rgba(227, 200, 153, 0.3);
                                 min-width: 130px; justify-content: center;
                                 font-size: 15px;'>
                        🟡 L2 低危
                    </span>
                    <span style='color: #5a6c7d; margin-left: 20px; font-size: 15px;'>单次违规+注意力低下<70%</span>
                </div>
                <div style='margin: 15px 0; display: flex; align-items: center;'>
                    <span style='background: linear-gradient(135deg, #a8c5b5 0%, #98b5a5 100%); 
                                 color: white; padding: 6px 18px; border-radius: 10px; 
                                 font-weight: 600; display: inline-flex; align-items: center;
                                 box-shadow: 0 3px 8px rgba(168, 197, 181, 0.3);
                                 min-width: 130px; justify-content: center;
                                 font-size: 15px;'>
                        🟢 L1 安全
                    </span>
                    <span style='color: #5a6c7d; margin-left: 20px; font-size: 15px;'>无违规+注意力低下<30%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_side:
        st.markdown("### 🔍 搜索", unsafe_allow_html=True)
        search_query = st.text_input("", placeholder="输入工人姓名、工号、区域...", label_visibility="collapsed",
                                     key="dashboard_search")

        if search_query and search_query.strip():
            results = search_workers(search_query, workers_df)
            if len(results) > 0:
                st.success(f"✅ 找到 {len(results)} 条结果")
                for idx, row in results.head(5).iterrows():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.98) 100%); 
                                padding: 15px; border-radius: 14px; margin: 10px 0; 
                                border-left: 4px solid #5a7199; 
                                box-shadow: 0 4px 16px rgba(90, 113, 153, 0.12);
                                backdrop-filter: blur(10px);
                                transition: all 0.3s ease;
                                position: relative; overflow: hidden;">
                        <div style="position: absolute; top: 0; right: 0; width: 100px; height: 100px;
                                    background: radial-gradient(circle, rgba(90,113,153,0.06) 0%, transparent 70%);
                                    pointer-events: none;"></div>
                        <div style="position: relative; z-index: 1;">
                            <div><strong style="font-size: 16px; color: #3d4f5e;">👤 {row["工人姓名"]}</strong> 
                            <span style="background: linear-gradient(135deg, #5a7199 0%, #667a9f 100%); 
                                         color: white; padding: 3px 10px; border-radius: 14px; 
                                         font-size: 11px; margin-left: 8px; font-weight: 600;
                                         box-shadow: 0 2px 6px rgba(90, 113, 153, 0.25);">{row["工号"]}</span></div>
                            <div style="margin-top: 10px; font-size: 13px; color: #5a6c7d; line-height: 1.6;">
                                💼 <span style="font-weight: 500;">{row["职位"]}</span> | 
                                📍 <span style="font-weight: 500;">{row["所在区域"]}</span> | 
                                🛡️ <span style="background: rgba(90,113,153,0.1); padding: 2px 8px; 
                                          border-radius: 6px; font-weight: 600;">{row["等级"]}</span>
                            </div>
                            <div style="margin-top: 8px; font-size: 12px; color: #95a5a6;">
                                ⚠️ 风险值: <span style="color: #c08080; font-weight: 600;">{row["风险值"]:.1f}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("❌ 未找到匹配结果")

        st.markdown("### 📅 2025年8月", unsafe_allow_html=True)

        calendar_html = """
        <style>
            .calendar-2025 {
                background: rgba(255, 255, 255, 0.97);
                padding: 15px;
                border-radius: 14px;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                border: 1px solid rgba(255, 255, 255, 0.9);
            }
            .calendar-header-2025 {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 8px;
                margin-bottom: 12px;
                font-weight: 600;
                text-align: center;
                color: #5a7199;
                font-size: 13px;
            }
            .calendar-days-2025 {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 6px;
            }
            .calendar-day-2025 {
                aspect-ratio: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 13px;
                font-weight: 500;
            }
            .calendar-day-2025:hover {
                background: #dfe7f2;
            }
            .today-2025 {
                background: #5a7fd6;
                color: white;
                font-weight: bold;
            }
        </style>
        <div class="calendar-2025">
            <div class="calendar-header-2025">
                <div>日</div><div>一</div><div>二</div><div>三</div>
                <div>四</div><div>五</div><div>六</div>
            </div>
            <div class="calendar-days-2025">
        """

        for _ in range(5):
            calendar_html += '<div></div>'

        current_day = 1
        for day in range(1, 32):
            if day == current_day:
                calendar_html += f'<div class="calendar-day-2025 today-2025">{day}</div>'
            else:
                calendar_html += f'<div class="calendar-day-2025">{day}</div>'

        calendar_html += "</div></div>"
        st.markdown(calendar_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### 🔔 预警通知", unsafe_allow_html=True)

        notifications = [
            {"title": "小C持续多天心理负荷较高", "icon": "⏰", "color": "#c4999d", "urgent": False},
            {"title": "小A心理负荷超30%", "action": "请立即核实", "icon": "⚠️", "color": "#d4af8f",
             "urgent": True},
            {"title": "小D报错,待核实", "icon": "🐛", "color": "#8b9dc3", "urgent": False},
            {"title": "小B存在异常波动,待监察", "icon": "📈", "color": "#8b9dc3", "urgent": False}
        ]

        for notif in notifications:
            urgent_text = f'<br><span style="color: {notif["color"]}; font-weight: 700; font-size: 13px;">▶ {notif.get("action", "")}</span>' if notif.get(
                "urgent") else ''
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.6); 
                        padding: 12px 16px; border-radius: 10px; 
                        border-left: 4px solid {notif['color']}; margin: 8px 0; 
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                        transition: all 0.3s ease;
                        position: relative; overflow: hidden;">
                <div style="position: absolute; top: 0; right: 0; width: 80px; height: 80px;
                            background: radial-gradient(circle, {notif['color']}08 0%, transparent 70%);
                            pointer-events: none;"></div>
                <div style="font-size: 14px; font-weight: 600; color: #3d4f5e; position: relative; z-index: 1;">
                    <span style="font-size: 16px; margin-right: 8px;">{notif['icon']}</span>{notif['title']}
                </div>
                {urgent_text}
            </div>
            """, unsafe_allow_html=True)


def render_alerts():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    workers_df, dates, risk_values, level_stable, level_unstable = generate_mock_data()

    st.markdown("### 📊 总体分析")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("#### 未来7天风险趋势图")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates, y=risk_values,
            mode='lines+markers',
            name='风险值',
            line=dict(color='#667eea', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))

        max_idx = risk_values.index(max(risk_values))
        fig.add_annotation(
            x=dates[max_idx], y=risk_values[max_idx],
            text=f"关键节点<br>{dates[max_idx]}混凝土浇筑<br>({risk_values[max_idx]}%高风险)",
            showarrow=True, arrowhead=2,
            bgcolor="rgba(255, 100, 100, 0.8)",
            font=dict(color="white")
        )

        fig.update_layout(
            xaxis_title="日期", yaxis_title="风险值(%)",
            height=400, hovermode='x unified',
            yaxis=dict(range=[0, 30]),
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True, config={
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                       'resetScale2d'],
            'displaylogo': False
        })
        st.info("📌 **关键节点:** 8月5日混凝土浇筑(24.5%高风险)")

    with col2:
        st.markdown("#### 各工人等级稳定与不稳定人数比例")

        labels, values, colors = [], [], []
        stable_colors = {'L1': '#4285f4', 'L2': '#fbbc04', 'L3': '#ea4335'}
        unstable_colors = {'L1': '#8ab4f8', 'L2': '#fdd663', 'L3': '#f28b82'}

        for level in ['L1', 'L2', 'L3']:
            labels.append(f'{level} 稳定')
            values.append(level_stable[level])
            colors.append(stable_colors[level])
            labels.append(f'{level} 不稳定')
            values.append(level_unstable[level])
            colors.append(unstable_colors[level])

        fig = go.Figure(data=[go.Pie(
            labels=labels, values=values, hole=0.4,
            marker=dict(colors=colors),
            textposition='auto', textinfo='label+percent'
        )])

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
            showlegend=True,
            height=350,
            paper_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True, config={
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'],
            'displaylogo': False
        })

    st.markdown("---")
    st.markdown("### ⚠️ 高风险工人名单")

    # 日期筛选
    col_date1, col_date2, col_btn, col_reset = st.columns([2, 2, 1, 1])
    with col_date1:
        start_date = st.date_input("开始日期",
                                   value=st.session_state.alert_start_date if st.session_state.alert_start_date else datetime.now() - timedelta(
                                       days=7),
                                   key="alert_start_date_input")
    with col_date2:
        end_date = st.date_input("结束日期",
                                 value=st.session_state.alert_end_date if st.session_state.alert_end_date else datetime.now(),
                                 key="alert_end_date_input")
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 筛选", use_container_width=True, key="filter_dates"):
            st.session_state.alert_start_date = start_date
            st.session_state.alert_end_date = end_date
            st.rerun()
    with col_reset:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 重置", use_container_width=True, key="reset_filter"):
            st.session_state.alert_start_date = None
            st.session_state.alert_end_date = None
            st.rerun()

    # 获取高风险工人并应用筛选
    high_risk_workers = workers_df[workers_df['风险值'] > 60].sort_values('风险值', ascending=False).copy()

    # 日期筛选
    if st.session_state.alert_start_date and st.session_state.alert_end_date:
        start_datetime = datetime.combine(st.session_state.alert_start_date, datetime.min.time())
        end_datetime = datetime.combine(st.session_state.alert_end_date, datetime.max.time())
        high_risk_workers = high_risk_workers[
            (high_risk_workers['预警时间'] >= start_datetime) &
            (high_risk_workers['预警时间'] <= end_datetime)
            ]
        st.info(
            f"📅 筛选时间段: {st.session_state.alert_start_date} 至 {st.session_state.alert_end_date}，共找到 {len(high_risk_workers)} 条记录")

    # 排除被忽略的工人
    high_risk_workers = high_risk_workers[~high_risk_workers['工人姓名'].isin(st.session_state.ignored_workers)]

    # 显示被忽略的工人数量和恢复按钮
    if len(st.session_state.ignored_workers) > 0:
        col_ignore_info, col_restore = st.columns([8, 2])
        with col_ignore_info:
            st.warning(f"⚠️ 已忽略 {len(st.session_state.ignored_workers)} 条预警记录")
        with col_restore:
            if st.button("🔄 恢复全部", use_container_width=True, key="restore_all"):
                st.session_state.ignored_workers = []
                st.session_state.show_analysis = {}
                st.success("✅ 已恢复所有忽略的记录")
                st.rerun()

    # 显示工人列表（紧凑布局）
    for idx, worker in high_risk_workers.iterrows():
        # 使用容器包裹每一行，减少间距
        with st.container():
            col_name, col_level, col_area, col_time, col_action = st.columns([2, 1, 2, 2, 3])

            with col_name:
                st.markdown(f"**{worker['工人姓名']}** ({worker['工号']})")
            with col_level:
                level_color = '#ff4444' if worker['等级'] == 'L3' else '#ffaa00' if worker[
                                                                                        '等级'] == 'L2' else '#00cc44'
                st.markdown(f"<span style='color: {level_color}; font-weight: bold;'>{worker['等级']}</span>",
                            unsafe_allow_html=True)
            with col_area:
                st.markdown(worker['所在区域'])
            with col_time:
                time_diff = datetime.now() - worker['预警时间']
                if time_diff.days > 0:
                    time_str = f"{time_diff.days}天前"
                elif time_diff.seconds // 3600 > 0:
                    time_str = f"{time_diff.seconds // 3600}小时前"
                else:
                    time_str = f"{time_diff.seconds // 60}分钟前"
                st.markdown(time_str)
            with col_action:
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("分析", key=f"analyze_{idx}", use_container_width=True):
                        # 生成针对性分析
                        if idx not in st.session_state.show_analysis:
                            st.session_state.show_analysis[idx] = True
                        else:
                            st.session_state.show_analysis[idx] = not st.session_state.show_analysis[idx]
                        st.rerun()
                with c2:
                    if st.button("干预", key=f"intervene_{idx}", use_container_width=True):
                        st.session_state.selected_worker = worker['工人姓名']
                        st.session_state.current_page = '干预措施'
                        st.rerun()
                with c3:
                    if st.button("忽略", key=f"ignore_{idx}", use_container_width=True):
                        st.session_state.ignored_workers.append(worker['工人姓名'])
                        if idx in st.session_state.show_analysis:
                            del st.session_state.show_analysis[idx]
                        st.success(f"✅ 已忽略 {worker['工人姓名']} 的预警")
                        st.rerun()

            # 显示分析结果
            if st.session_state.show_analysis.get(idx, False):
                analysis = generate_ai_analysis(worker['工人姓名'], worker, st.session_state.intervention_records)
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                            padding: 20px; border-radius: 12px; margin: 10px 0 15px 0;
                            border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
                    <div style='font-weight: bold; color: #667eea; margin-bottom: 12px; font-size: 15px;'>
                        🤖 AI智能分析 - {worker['工人姓名']}
                    </div>
                    <div style='color: #333; line-height: 1.8; font-size: 13px; white-space: pre-wrap;'>
{analysis}
                    </div>
                    <div style='margin-top: 15px; padding-top: 12px; border-top: 1px solid #dee2e6;'>
                        <strong style='color: #666;'>📊 详细数据:</strong><br>
                        <span style='color: #666; font-size: 12px;'>
                        风险值: {worker['风险值']:.1f} | 疲劳度: {worker['疲劳度']:.1f} | 注意力: {worker['注意力']:.1f} | 
                        年龄: {worker['年龄']}岁 | 职位: {worker['职位']} | 预警时间: {worker['预警时间'].strftime('%Y-%m-%d %H:%M')}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 使用更小的分隔线
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if len(high_risk_workers) == 0:
        st.success("✅ 当前时间段内没有高风险工人！")


def render_interventions():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    workers_df, _, _, _, _ = generate_mock_data()

    col_main, col_side = st.columns([7, 3])

    with col_main:
        col_worker, col_schedule = st.columns([0.8, 1.2],gap="small")

        with col_worker:
            worker_info = workers_df[workers_df['工人姓名'] == st.session_state.selected_worker].iloc[0]

            st.markdown(f"""
            <div class="blue-gradient-card" style="width: 253px; height: 295px; padding: 15px; box-sizing: border-box;">
                <h3 style='text-align: center; margin: 0 0 12px 0; font-size: 18px;'>工人基本情况</h3>
                <div style='display: flex; gap: 12px; align-items: flex-start;'>
                    <div style='flex-shrink: 0; text-align: center;'>
                        <div style='font-size: 60px; line-height: 1; margin-bottom: 8px;'>👷</div>
                        <div style='background: white; color: #5a7fd6; padding: 4px 10px; border-radius: 8px; 
                                    font-weight: bold; font-size: 16px; white-space: nowrap;'>
                            {worker_info['等级']}
                        </div>
                    </div>
                    <div style='flex: 1; line-height: 1.7; font-size: 12.5px; padding-top: 4px;'>
                        <p style='margin: 3px 0;'><strong>姓名:</strong> {worker_info['工人姓名']}</p>
                        <p style='margin: 3px 0;'><strong>年龄:</strong> {worker_info['年龄']}岁</p>
                        <p style='margin: 3px 0;'><strong>工号:</strong> {worker_info['工号']}</p>
                        <p style='margin: 3px 0;'><strong>职位:</strong> {worker_info['职位']}</p>
                        <p style='margin: 3px 0;'><strong>所在区域:</strong> {worker_info['所在区域']}</p>
                        <p style='margin: 3px 0;'><strong>紧急联系人:</strong> {worker_info['紧急联系人']}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_schedule:
            st.markdown("""
            <div style='background: white; padding: 20px; border-radius: 10px; 
                        border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h3 style='color: #667eea; margin-bottom: 15px; font-size: 20px;'>智能排程优化</h3>
                <p style='margin-bottom: 20px; font-size: 15px;'><strong>原计划:</strong> A区全天高空作业</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 15px;'>", unsafe_allow_html=True)

            check1 = st.checkbox("高风险时段改地面作业",
                                 value=st.session_state.optimize_checkbox1,
                                 key="opt_check1")
            if check1 != st.session_state.optimize_checkbox1:
                st.session_state.optimize_checkbox1 = check1
                st.success("✓ 已调整为地面作业" if check1 else "✗ 取消调整")

            check2 = st.checkbox("调至低风险班组",
                                 value=st.session_state.optimize_checkbox2,
                                 key="opt_check2")
            if check2 != st.session_state.optimize_checkbox2:
                st.session_state.optimize_checkbox2 = check2
                st.success("✓ 已调整班组" if check2 else "✗ 取消调整")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        tab_col1, tab_col2, tab_col3 = st.columns([1.2, 1.2, 7.6])
        with tab_col1:
            if st.button("📋 干预计划",
                         type="primary" if st.session_state.intervention_tab == '干预计划' else "secondary",
                         use_container_width=True):
                st.session_state.intervention_tab = '干预计划'
                st.rerun()
        with tab_col2:
            if st.button("📝 干预记录",
                         type="primary" if st.session_state.intervention_tab == '干预记录' else "secondary",
                         use_container_width=True):
                st.session_state.intervention_tab = '干预记录'
                st.rerun()

        if st.session_state.intervention_tab == '干预计划':
            st.markdown("""
            <div class="white-card" style='margin-top: 20px;'>
                <p style='font-size: 16px;'>
                    <strong>干预计划</strong> 共4次干预计划,
                    <span style='color: green;'>已完成2次</span>,
                    <span style='color: orange;'>即将干预1次</span>,
                    <span style='color: gray;'>未干预1次</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

            plan1_expanded = st.expander("📋 计划1: 2025-08-05 - 即将干预", expanded=True)
            with plan1_expanded:
                if st.session_state.editing_plan == 'plan1':
                    st.markdown("#### 📝 编辑计划")

                    new_time = st.text_input("计划干预时间",
                                             value=st.session_state.plan_data['plan1']['time'],
                                             key="edit_time1")
                    new_analysis = st.text_area("动机分析",
                                                value=st.session_state.plan_data['plan1']['analysis'],
                                                key="edit_analysis1",
                                                height=80)
                    new_measure = st.text_area("干预措施",
                                               value=st.session_state.plan_data['plan1']['measure'],
                                               key="edit_measure1",
                                               height=80)
                    new_effect = st.text_input("预期效果",
                                               value=st.session_state.plan_data['plan1']['effect'],
                                               key="edit_effect1")
                    new_result = st.text_input("干预结果",
                                               value=st.session_state.plan_data['plan1']['result'],
                                               key="edit_result1")

                    col_save, col_cancel = st.columns([1, 1])
                    with col_save:
                        if st.button("💾 保存", key="save_plan1", use_container_width=True, type="primary"):
                            st.session_state.plan_data['plan1']['time'] = new_time
                            st.session_state.plan_data['plan1']['analysis'] = new_analysis
                            st.session_state.plan_data['plan1']['measure'] = new_measure
                            st.session_state.plan_data['plan1']['effect'] = new_effect
                            st.session_state.plan_data['plan1']['result'] = new_result

                            record = {
                                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'worker': st.session_state.selected_worker,
                                'plan_time': new_time,
                                'analysis': new_analysis,
                                'measure': new_measure,
                                'effect': new_effect,
                                'result': new_result
                            }
                            st.session_state.intervention_records.append(record)

                            st.session_state.editing_plan = None
                            st.success("✅ 保存成功! 已添加到干预记录")
                            st.rerun()
                    with col_cancel:
                        if st.button("❌ 取消", key="cancel_plan1", use_container_width=True):
                            st.session_state.editing_plan = None
                            st.rerun()
                else:
                    col_info, col_btn = st.columns([8, 2])
                    with col_info:
                        plan1 = st.session_state.plan_data['plan1']
                        st.markdown(f"""
                        - **计划干预时间:** {plan1['time']}
                        - **动机分析:** {plan1['analysis']}
                        - **干预措施:** {plan1['measure']}
                        - **预期效果:** {plan1['effect']}
                        - **干预结果:** <span style='color: orange; font-weight: bold;'>{plan1['result']}</span>
                        """, unsafe_allow_html=True)
                    with col_btn:
                        if st.button("✏️ 修改", key="modify_plan1", use_container_width=True):
                            st.session_state.editing_plan = 'plan1'
                            st.rerun()

            plan2_expanded = st.expander("📋 计划2: 2025-08-03 - 待执行", expanded=False)
            with plan2_expanded:
                if st.session_state.editing_plan == 'plan2':
                    st.markdown("#### 📝 编辑计划")

                    new_time = st.text_input("预计干预时间",
                                             value=st.session_state.plan_data['plan2']['time'],
                                             key="edit_time2")
                    new_analysis = st.text_area("动机分析",
                                                value=st.session_state.plan_data['plan2']['analysis'],
                                                key="edit_analysis2",
                                                height=80)
                    new_measure = st.text_area("干预措施",
                                               value=st.session_state.plan_data['plan2']['measure'],
                                               key="edit_measure2",
                                               height=80)

                    col_save, col_cancel = st.columns([1, 1])
                    with col_save:
                        if st.button("💾 保存", key="save_plan2", use_container_width=True, type="primary"):
                            st.session_state.plan_data['plan2']['time'] = new_time
                            st.session_state.plan_data['plan2']['analysis'] = new_analysis
                            st.session_state.plan_data['plan2']['measure'] = new_measure

                            record = {
                                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'worker': st.session_state.selected_worker,
                                'plan_time': new_time,
                                'analysis': new_analysis,
                                'measure': new_measure,
                                'effect': '',
                                'result': '待执行'
                            }
                            st.session_state.intervention_records.append(record)

                            st.session_state.editing_plan = None
                            st.success("✅ 保存成功! 已添加到干预记录")
                            st.rerun()
                    with col_cancel:
                        if st.button("❌ 取消", key="cancel_plan2", use_container_width=True):
                            st.session_state.editing_plan = None
                            st.rerun()
                else:
                    col_info, col_btn = st.columns([8, 2])
                    with col_info:
                        plan2 = st.session_state.plan_data['plan2']
                        st.markdown(f"""
                        - **预计干预时间:** {plan2['time']}
                        - **动机分析:** {plan2['analysis']}
                        - **干预措施:** {plan2['measure']}
                        """, unsafe_allow_html=True)
                    with col_btn:
                        if st.button("✏️ 修改", key="modify_plan2", use_container_width=True):
                            st.session_state.editing_plan = 'plan2'
                            st.rerun()

        else:
            if len(st.session_state.intervention_records) == 0:
                st.info("📝 暂无干预记录")
            else:
                st.markdown(f"""
                <div class="white-card" style='margin-top: 20px;'>
                    <p style='font-size: 16px;'>
                        <strong>干预记录</strong> 共 {len(st.session_state.intervention_records)} 条记录
                    </p>
                </div>
                """, unsafe_allow_html=True)

                for idx, record in enumerate(reversed(st.session_state.intervention_records)):
                    with st.expander(
                            f"📝 记录{len(st.session_state.intervention_records) - idx}: {record['worker']} - {record['time']}",
                            expanded=False):
                        st.markdown(f"""
                        - **工人姓名:** {record['worker']}
                        - **记录时间:** {record['time']}
                        - **计划干预时间:** {record['plan_time']}
                        - **动机分析:** {record['analysis']}
                        - **干预措施:** {record['measure']}
                        - **预期效果:** {record['effect'] if record['effect'] else '无'}
                        - **干预结果:** <span style='color: {"orange" if record["result"] == "即将干预" else "green" if record["result"] == "已完成" else "gray"}; font-weight: bold;'>{record['result']}</span>
                        """, unsafe_allow_html=True)

    with col_side:
        st.markdown("### 📅 2025年8月")
        render_calendar(highlighted_dates=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

        st.markdown("### 🤖 AI智能分析")

        if 'ai_analysis_result' not in st.session_state:
            st.session_state.ai_analysis_result = None

        if st.button("🔍 生成AI分析报告", use_container_width=True, type="primary"):
            worker_info = workers_df[workers_df['工人姓名'] == st.session_state.selected_worker].iloc[0]
            analysis = generate_ai_analysis(
                st.session_state.selected_worker,
                worker_info,
                st.session_state.intervention_records
            )
            st.session_state.ai_analysis_result = analysis
            st.success("✅ 分析完成！")

        if st.session_state.ai_analysis_result:
            st.markdown(f"""
                    <div class="white-card">
                        <p><strong>🤖 AI分析结果</strong></p>
                        <div style='color: #333; margin: 10px 0; line-height: 1.8; font-size: 13px; white-space: pre-wrap;'>
        {st.session_state.ai_analysis_result}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("🗑️ 清除分析", use_container_width=True):
                st.session_state.ai_analysis_result = None
                st.rerun()
        else:
            st.markdown("""
                    <div class="white-card">
                        <p><strong>1.干预记录</strong></p>
                        <p style='color: #667eea; margin: 8px 0;'>违规共下降63%</p>
                        <p style='color: #667eea; margin: 8px 0;'>冲突共下降45%</p>
                        <p style='color: #667eea; margin: 8px 0;'>疲劳事故共下降54%</p>
                        <br>
                        <p><strong>2.干预计划</strong></p>
                        <p style='color: #667eea; margin: 8px 0;'>预计在五天后 (2025-08-05) 完成干预</p>
                    </div>
                    """, unsafe_allow_html=True)

        # 修改3: 详情按钮弹出详细分析报告
        if st.button("📊 详情", use_container_width=True):
            st.session_state.show_detail_dialog = not st.session_state.show_detail_dialog
            st.rerun()

        if st.session_state.show_detail_dialog:
            with st.expander("📈 详细分析报告", expanded=True):
                worker_info = workers_df[workers_df['工人姓名'] == st.session_state.selected_worker].iloc[0]

                st.markdown("#### 🔍 综合评估")
                st.markdown(f"""
                - **工人姓名**: {st.session_state.selected_worker}
                - **风险等级**: {worker_info['等级']}
                - **当前风险值**: {worker_info['风险值']:.1f}
                - **疲劳度**: {worker_info['疲劳度']:.1f}
                - **注意力**: {worker_info['注意力']:.1f}
                """)

                st.markdown("---")
                st.markdown("#### 📊 干预效果统计")
                col_eff1, col_eff2, col_eff3 = st.columns(3)
                with col_eff1:
                    st.metric("违规下降", "63%", "-37%")
                with col_eff2:
                    st.metric("冲突下降", "45%", "-25%")
                with col_eff3:
                    st.metric("疲劳事故", "54%", "-18%")

                st.markdown("---")
                st.markdown("#### 🎯 建议措施")
                st.markdown("""
                1. **短期措施**：调整作业安排，避免高风险时段作业
                2. **中期措施**：加强安全培训，提升安全意识
                3. **长期措施**：建立个人安全档案，持续跟踪改善
                """)

                st.markdown("---")
                st.markdown("#### 📅 预计完成时间")
                st.info("根据当前干预计划，预计在5天后（2025-08-05）完成主要干预措施")

                if st.button("关闭详情", use_container_width=True):
                    st.session_state.show_detail_dialog = False
                    st.rerun()


def render_progress():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    if 'progress_projects_data' not in st.session_state:
        st.session_state.progress_projects_data = {
            '一级项目': {
                'waiting': 34, 'ongoing': 78, 'unhandled': 57,
                'daily_progress': 65, 'total_progress': (8, 12),
                'sub_projects': [
                    {'name': '主体结构', 'value': 55}, {'name': '地基处理', 'value': 90},
                    {'name': '交通配套', 'value': 85}, {'name': '土方工程', 'value': 65}
                ],
                'issues': {'建材浪费': {'solved': 23, 'total': 52}, '安全隐患': {'solved': 46, 'total': 62}},
                'interventions': [
                    {'序号': 1, '干预日期': '2025/8/15', '工人姓名': 'A', '等级': 'L3', '干预措施': '强制下工'},
                    {'序号': 2, '干预日期': '2025/8/13', '工人姓名': 'B', '等级': 'L2',
                     '干预措施': '调离发起者至其他班组'},
                    {'序号': 3, '干预日期': '2025/8/13', '工人姓名': 'C', '等级': 'L3', '干预措施': '停工暂休'},
                    {'序号': 4, '干预日期': '2025/8/8', '工人姓名': 'D', '等级': 'L2', '干预措施': '认知重塑训练'},
                    {'序号': 5, '干预日期': '2025/8/4', '工人姓名': 'E', '等级': 'L1',
                     '干预措施': '智能耳机播放提神音效'},
                    {'序号': 6, '干预日期': '2025/8/4', '工人姓名': 'F', '等级': 'L3', '干预措施': '停工暂休'},
                    {'序号': 7, '干预日期': '2025/8/2', '工人姓名': 'G', '等级': 'L1', '干预措施': '事故体验训练'}
                ]
            },
            '二级项目': {
                'waiting': 28, 'ongoing': 65, 'unhandled': 43,
                'daily_progress': 72, 'total_progress': (6, 10),
                'sub_projects': [
                    {'name': '钢结构安装', 'value': 68}, {'name': '电气工程', 'value': 75},
                    {'name': '给排水', 'value': 80}, {'name': '暖通工程', 'value': 62}
                ],
                'issues': {'建材浪费': {'solved': 18, 'total': 45}, '安全隐患': {'solved': 35, 'total': 50}},
                'interventions': [
                    {'序号': 1, '干预日期': '2025/8/14', '工人姓名': 'H', '等级': 'L2', '干预措施': '安全培训'},
                    {'序号': 2, '干预日期': '2025/8/12', '工人姓名': 'I', '等级': 'L1', '干预措施': '岗位调整'},
                    {'序号': 3, '干预日期': '2025/8/10', '工人姓名': 'J', '等级': 'L3', '干预措施': '强制休息'},
                    {'序号': 4, '干预日期': '2025/8/7', '工人姓名': 'K', '等级': 'L2', '干预措施': '心理疏导'},
                    {'序号': 5, '干预日期': '2025/8/5', '工人姓名': 'L', '等级': 'L1', '干预措施': '技能培训'}
                ]
            },
            '三级项目': {
                'waiting': 45, 'ongoing': 92, 'unhandled': 68,
                'daily_progress': 58, 'total_progress': (9, 15),
                'sub_projects': [
                    {'name': '装饰装修', 'value': 45}, {'name': '景观绿化', 'value': 60},
                    {'name': '智能化系统', 'value': 70}, {'name': '消防工程', 'value': 55}
                ],
                'issues': {'建材浪费': {'solved': 30, 'total': 60}, '安全隐患': {'solved': 50, 'total': 75}},
                'interventions': [
                    {'序号': 1, '干预日期': '2025/8/16', '工人姓名': 'M', '等级': 'L3', '干预措施': '停工整改'},
                    {'序号': 2, '干预日期': '2025/8/14', '工人姓名': 'N', '等级': 'L2', '干预措施': '班组调整'},
                    {'序号': 3, '干预日期': '2025/8/11', '工人姓名': 'O', '等级': 'L3', '干预措施': '强制下工'},
                    {'序号': 4, '干预日期': '2025/8/9', '工人姓名': 'P', '等级': 'L1', '干预措施': '健康检查'},
                    {'序号': 5, '干预日期': '2025/8/6', '工人姓名': 'Q', '等级': 'L2', '干预措施': '安全教育'},
                    {'序号': 6, '干预日期': '2025/8/3', '工人姓名': 'R', '等级': 'L3', '干预措施': '设备检修'}
                ]
            },
            '四级项目': {
                'waiting': 21, 'ongoing': 56, 'unhandled': 35,
                'daily_progress': 80, 'total_progress': (5, 8),
                'sub_projects': [
                    {'name': '外墙涂装', 'value': 88}, {'name': '道路铺设', 'value': 92},
                    {'name': '围墙建设', 'value': 78}, {'name': '标识标牌', 'value': 85}
                ],
                'issues': {'建材浪费': {'solved': 15, 'total': 38}, '安全隐患': {'solved': 28, 'total': 42}},
                'interventions': [
                    {'序号': 1, '干预日期': '2025/8/15', '工人姓名': 'S', '等级': 'L1', '干预措施': '技能提升'},
                    {'序号': 2, '干预日期': '2025/8/12', '工人姓名': 'T', '等级': 'L2', '干预措施': '安全提醒'},
                    {'序号': 3, '干预日期': '2025/8/9', '工人姓名': 'U', '等级': 'L1', '干预措施': '定期检查'},
                    {'序号': 4, '干预日期': '2025/8/6', '工人姓名': 'V', '等级': 'L2', '干预措施': '休息调整'}
                ]
            }
        }
        if 'project_name_mapping' not in st.session_state:
            st.session_state.project_name_mapping = {
                '主体结构': '一级项目',
                '地基处理': '一级项目',
                '交通配套': '一级项目',
                '土方工程': '一级项目',
                '钢结构安装': '二级项目',
                '电气工程': '二级项目',
                '给排水': '二级项目',
                '暖通工程': '二级项目',
                '装饰装修': '三级项目',
                '景观绿化': '三级项目',
                '智能化系统': '三级项目',
                '消防工程': '三级项目',
                '外墙涂装': '四级项目',
                '道路铺设': '四级项目',
                '围墙建设': '四级项目',
                '标识标牌': '四级项目'
            }

    if 'show_progress_detail' not in st.session_state:
        st.session_state.show_progress_detail = False

    current_level = st.session_state.progress_level
    current_data = st.session_state.progress_projects_data[current_level]
    if 'progress_filter_date' not in st.session_state:
        st.session_state.progress_filter_date = None
    if 'progress_filter_name' not in st.session_state:
        st.session_state.progress_filter_name = ''

    col1, col2, col3 = st.columns(3)
    cards_data = [
        ("待干预工人人数", current_data['waiting'], "#6b8fd9"),
        ("干预中工人人数", current_data['ongoing'], "#7b9ae3"),
        ("未干预工人人数", current_data['unhandled'], "#8ba5ed")
    ]

    for col, (label, value, color) in zip([col1, col2, col3], cards_data):
        with col:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                        padding: 25px 20px; border-radius: 20px; color: white; text-align: center;
                        box-shadow: 0 4px 12px rgba(107, 143, 217, 0.3);
                        min-height: 120px; display: flex; flex-direction: column; justify-content: center;'>
                <div style='display: flex; align-items: center; justify-content: center; gap: 10px;'>
                    <div style='font-size: 24px;'>👷</div>
                    <div style='font-size: 16px; font-weight: 600;'>{label}</div>
                </div>
                <div style='font-size: 48px; font-weight: bold; margin-top: 10px;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([7, 3])

    with col_main:
        intervention_list = current_data['interventions']

        st.markdown("""
        <div style='padding: 20px;'>
        """, unsafe_allow_html=True)

        col_header = st.columns([0.8, 1.5, 1.2, 1, 3, 0.8])
        headers = ['序号', '干预日期', '工人姓名', '等级', '干预措施', '进度']
        for col_h, header in zip(col_header, headers):
            with col_h:
                st.markdown(
                    f"<div style='font-weight: bold; color: #666; font-size: 14px; padding: 8px 0;'>{header}</div>",
                    unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

        if f'filtered_interventions_{current_level}' in st.session_state:
            intervention_list = st.session_state[f'filtered_interventions_{current_level}']
            if len(intervention_list) == 0:
                st.info("📝 未找到符合条件的记录")

        for idx, row in enumerate(intervention_list):
            cols = st.columns([0.8, 1.5, 1.2, 1, 3, 0.8])

            with cols[0]:
                st.markdown(f"<div style='padding: 8px 0;'>{row['序号']}</div>", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"<div style='padding: 8px 0;'>{row['干预日期']}</div>", unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"<div style='padding: 8px 0;'>{row['工人姓名']}</div>", unsafe_allow_html=True)
            with cols[3]:
                level_colors = {'L3': '#ff4444', 'L2': '#ffaa00', 'L1': '#00cc44'}
                st.markdown(
                    f"<div style='padding: 8px 0; color: {level_colors[row['等级']]}; font-weight: bold;'>{row['等级']}</div>",
                    unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f"<div style='padding: 8px 0;'>{row['干预措施']}</div>", unsafe_allow_html=True)
            with cols[5]:
                st.checkbox("", key=f"progress_check_{current_level}_{idx}", label_visibility="collapsed")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='padding: 20px;'>
        """, unsafe_allow_html=True)

        search_col1, search_col2 = st.columns([1, 1])

        with search_col1:
            st.markdown("<div style='margin-bottom: 8px; font-weight: 600; color: #333;'>日期</div>",
                        unsafe_allow_html=True)
            st.markdown("<div style='font-size: 12px; color: #999; margin-bottom: 5px;'>请选择日期（例如8月15日）</div>",
                        unsafe_allow_html=True)
            date_input = st.date_input("", datetime(2025, 8, 15), label_visibility="collapsed",
                                       key=f"date_input_{current_level}")

        with search_col2:
            st.markdown("<div style='margin-bottom: 8px; font-weight: 600; color: #333;'>项目名称</div>",
                        unsafe_allow_html=True)
            st.markdown("<div style='font-size: 12px; color: #999; margin-bottom: 5px;'>输入工人姓名或措施关键词</div>",
                        unsafe_allow_html=True)
            project_input = st.text_input("", placeholder="例如: A, 强制, 培训", label_visibility="collapsed",
                                          key=f"project_input_{current_level}",
                                          value=st.session_state.progress_filter_name)

        st.markdown("<div style='margin-top: 15px; margin-bottom: 8px; font-weight: 600; color: #333;'>查询</div>",
                    unsafe_allow_html=True)

        col_search_btn, col_reset_btn, col_empty = st.columns([1, 1, 8])

        with col_search_btn:
            if st.button("🔍 查询", use_container_width=True, key=f"search_btn_{current_level}"):
                from datetime import datetime as dt

                query_project = project_input.strip() if project_input else None
                filtered_interventions = current_data['interventions'].copy()

                if date_input:
                    user_date = dt.combine(date_input, dt.min.time())
                    temp_filtered = []
                    for item in filtered_interventions:
                        try:
                            item_date = dt.strptime(item['干预日期'], '%Y/%m/%d')
                            if item_date >= user_date:
                                temp_filtered.append(item)
                        except:
                            temp_filtered.append(item)
                    filtered_interventions = temp_filtered

                if query_project:
                    if query_project in st.session_state.project_name_mapping:
                        matched_level = st.session_state.project_name_mapping[query_project]
                        if matched_level != st.session_state.progress_level:
                            st.session_state.progress_level = matched_level
                            st.success(f"✅ 已切换到 {matched_level}，项目：{query_project}")
                            st.rerun()
                        else:
                            st.success(f"✅ 查询完成：{query_project}（当前级别）")
                    else:
                        temp_filtered = []
                        for item in filtered_interventions:
                            if query_project.lower() in str(item['工人姓名']).lower() or \
                                    query_project.lower() in str(item['干预措施']).lower():
                                temp_filtered.append(item)
                        filtered_interventions = temp_filtered

                        if len(filtered_interventions) == 0:
                            st.warning(f"⚠️ 未找到关键词 '{query_project}'")
                        else:
                            st.success(f"✅ 找到 {len(filtered_interventions)} 条记录")
                else:
                    if date_input:
                        st.success(f"✅ 找到 {len(filtered_interventions)} 条记录")

                st.session_state[f'filtered_interventions_{current_level}'] = filtered_interventions
                st.session_state.progress_filter_date = date_input
                st.session_state.progress_filter_name = project_input
                st.rerun()

        with col_reset_btn:
            if st.button("🔄 重置", use_container_width=True, key=f"reset_btn_{current_level}"):
                st.session_state.progress_filter_date = None
                st.session_state.progress_filter_name = ''
                if f'filtered_interventions_{current_level}' in st.session_state:
                    del st.session_state[f'filtered_interventions_{current_level}']
                st.success("✅ 已重置")
                st.rerun()

        if st.session_state.progress_filter_date or st.session_state.progress_filter_name:
            filter_info = []
            if st.session_state.progress_filter_date:
                filter_info.append(f"📅 日期: 8月{st.session_state.progress_filter_date.day}日")
            if st.session_state.progress_filter_name:
                filter_info.append(f"🔍 关键词: {st.session_state.progress_filter_name}")

            matched_count = len(intervention_list)
            total_count = len(current_data['interventions'])

            st.markdown(f"""
                    <div style='margin-top: 10px; padding: 12px; background: #e8f5e9; border-radius: 6px; border-left: 4px solid #4caf50;'>
                        <div style='font-size: 14px; color: #2e7d32; font-weight: 600;'>
                            ✅ 查询结果: 找到 {matched_count} 条记录（共 {total_count} 条）
                        </div>
                        <div style='font-size: 12px; color: #555; margin-top: 5px;'>
                            {' | '.join(filter_info)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        level_cols = st.columns([1, 1, 1, 1, 4])
        levels = ['一级项目', '二级项目', '三级项目', '四级项目']

        for col, level in zip(level_cols[:4], levels):
            with col:
                btn_type = "primary" if st.session_state.progress_level == level else "secondary"
                if st.button(level, type=btn_type, use_container_width=True, key=f"level_btn_{level}"):
                    if st.session_state.progress_level != level:
                        st.session_state.progress_level = level
                        st.session_state.progress_filter_date = None
                        st.session_state.progress_filter_name = ''
                        for key in list(st.session_state.keys()):
                            if key.startswith('filtered_interventions_'):
                                del st.session_state[key]
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        progress_col1, progress_col2, progress_col3 = st.columns([2.5, 2.5, 5])

        with progress_col1:
            st.markdown(f"""
            <div style='background: white; padding: 30px 20px; border-radius: 12px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;'>
                <div style='font-size: 72px; font-weight: bold; color: #6b8fd9; line-height: 1;'>{current_data['daily_progress']}%</div>
                <div style='font-size: 16px; color: #666; margin-top: 15px; font-weight: 500;'>今日工程进度</div>
            </div>
            """, unsafe_allow_html=True)

        with progress_col2:
            month, total = current_data['total_progress']
            st.markdown(f"""
            <div style='background: white; padding: 30px 20px; border-radius: 12px; 
                        box-shadow: 0 2px 8px rgba(0,0,0,0.08); text-align: center;'>
                <div style='font-size: 72px; font-weight: bold; color: #6b8fd9; line-height: 1;'>
                    {month}<span style='font-size: 36px;'>/{total}月</span>
                </div>
                <div style='font-size: 16px; color: #666; margin-top: 15px; font-weight: 500;'>总工程进度</div>
            </div>
            """, unsafe_allow_html=True)

        with progress_col3:
            projects = current_data['sub_projects']

            # 将四个环状图放到一排
            col_p1, col_p2, col_p3, col_p4 = st.columns(4)
            cols_list = [col_p1, col_p2, col_p3, col_p4]
            colors = ['#ff6b6b', '#ee5a6f', '#f06595', '#cc5de8']

            for col_p, project, color in zip(cols_list, projects, colors):
                with col_p:
                    percentage = project['value']
                    circumference = 2 * 3.14159 * 40
                    dasharray = (percentage / 100) * circumference

                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px;'>
                        <div style='position: relative; width: 100px; height: 100px; margin: 0 auto;'>
                            <svg width="100" height="100" viewBox="0 0 100 100" style='transform: rotate(-90deg);'>
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#e0e0e0" stroke-width="8"/>
                                <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="8"
                                        stroke-dasharray="{dasharray} {circumference}"
                                        stroke-linecap="round"/>
                            </svg>
                            <div style='position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                                        font-size: 20px; font-weight: bold; color: #333;'>
                                {percentage}%
                            </div>
                        </div>
                        <div style='margin-top: 10px; font-size: 14px; color: #666; font-weight: 500;'>
                            {project['name']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with col_side:
        st.markdown("### 📅 2025年8月")
        render_calendar(highlighted_dates=list(range(2, 30)))

        st.markdown("<br>", unsafe_allow_html=True)

        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            btn_type_issues = "primary" if not st.session_state.show_progress_detail else "secondary"
            if st.button("问题清单", type=btn_type_issues, use_container_width=True, key=f"tab_issues_{current_level}"):
                st.session_state.show_progress_detail = False
                st.rerun()
        with tab_col2:
            btn_type_details = "primary" if st.session_state.show_progress_detail else "secondary"
            if st.button("详情", type=btn_type_details, use_container_width=True, key=f"tab_details_{current_level}"):
                st.session_state.show_progress_detail = True
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.show_progress_detail:
            issues = current_data['issues']
            total_issues = sum(item['total'] for item in issues.values())
            solved_issues = sum(item['solved'] for item in issues.values())
            solve_rate = int((solved_issues / total_issues) * 100) if total_issues > 0 else 0

            st.markdown("### 📊 " + current_level + "详情报告")

            col_detail1, col_detail2 = st.columns(2)

            with col_detail1:
                st.metric("项目进度", f"{current_data['daily_progress']}%")
                st.metric("问题解决率", f"{solve_rate}%",
                          delta=f"已解决 {solved_issues}/{total_issues} 个问题")

            with col_detail2:
                st.markdown("**干预统计**")
                stat_col1, stat_col2, stat_col3 = st.columns(3)
                with stat_col1:
                    st.metric("待干预", current_data['waiting'])
                with stat_col2:
                    st.metric("干预中", current_data['ongoing'])
                with stat_col3:
                    st.metric("未干预", current_data['unhandled'])

            st.markdown("---")

            st.warning(f"""
        **⚠️ 重点关注：**
        - {list(issues.keys())[0]}问题需加强管理
        - 建议增加安全巡查频次  
        - 加强工人安全教育培训
                    """)
        else:
            issues = current_data['issues']

            st.markdown("""
            <div style='padding: 20px;'>
            """, unsafe_allow_html=True)

            for issue_name, issue_data in issues.items():
                solved = issue_data['solved']
                total = issue_data['total']
                percentage = int((solved / total) * 100)

                st.markdown(f"""
                <div style='margin-bottom: 25px;'>
                    <div style='font-weight: 600; font-size: 15px; color: #333; margin-bottom: 12px;'>{issue_name}</div>
                    <div style='color: #666; font-size: 14px; margin-bottom: 10px;'>
                        已解决<span style='color: #6b8fd9; font-weight: bold;'>{solved}</span>/{total}
                    </div>
                    <div style='background: #e8f0ff; height: 12px; border-radius: 6px; overflow: hidden;'>
                        <div style='background: linear-gradient(90deg, #6b8fd9 0%, #5a7fd6 100%); 
                                    height: 100%; width: {percentage}%; border-radius: 6px;'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


def render_individual_analysis():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    workers_df, _, _, _, _ = generate_mock_data()

    # 工人选择器
    col_select, col_empty = st.columns([3, 7])
    with col_select:
        worker_names = workers_df['工人姓名'].tolist()
        selected_index = worker_names.index(
            st.session_state.selected_worker) if st.session_state.selected_worker in worker_names else 0
        selected_worker = st.selectbox(
            "选择工人",
            worker_names,
            index=selected_index,
            key="individual_worker_select"
        )
        if selected_worker != st.session_state.selected_worker:
            st.session_state.selected_worker = selected_worker
            st.rerun()

    # 获取当前选中的工人信息
    worker_info = workers_df[workers_df['工人姓名'] == st.session_state.selected_worker].iloc[0]

    # 根据不同工人生成不同的数据
    import hashlib
    worker_hash = int(hashlib.md5(worker_info['工人姓名'].encode()).hexdigest(), 16)
    np.random.seed(worker_hash % 10000)

    # 生成该工人的特定数据
    mental_levels = [np.random.uniform(0.5, 4.5) for _ in range(6)]
    risk_values = [
        np.random.uniform(35, 55),  # 生理
        np.random.uniform(10, 25),  # 行为
        np.random.uniform(15, 30),  # 环境
        np.random.uniform(5, 15)  # 文本
    ]
    predict_prob = np.random.randint(50, 85)
    similarity = np.random.randint(60, 90)

    # 生成状态识别需要的数据
    heart_rate = np.random.randint(70, 110)
    fatigue = np.random.choice(['低', '中等', '偏高'])
    emotion_status = np.random.choice(['焦虑', '平静', '紧张', '疲惫'])
    speech_rate = np.random.randint(120, 180)

    # 创建左右两列布局
    col_left, col_right = st.columns([6, 4])

    with col_left:
        # 修改1: 工人基本情况卡片（宽度减小 - 添加max-width: 600px）
        st.markdown(f"""
        <div class="blue-gradient-card" style="margin-bottom: 20px; max-width: 600px;">
            <h3 style='text-align: center; margin: 0 0 20px 0; font-size: 20px;'>工人基本情况</h3>
            <div style='display: flex; gap: 20px; align-items: flex-start;'>
                <div style='flex-shrink: 0; text-align: center;'>
                    <div style='font-size: 80px; line-height: 1; margin-bottom: 10px;'>👷</div>
                    <div style='background: white; color: #5a7fd6; padding: 8px 20px; border-radius: 12px; 
                                font-weight: bold; font-size: 18px; white-space: nowrap;'>
                        {worker_info['等级']}
                    </div>
                </div>
                <div style='flex: 1; line-height: 1.8; font-size: 14px;'>
                    <p style='margin: 4px 0;'><strong>姓名:</strong> {worker_info['工人姓名']}</p>
                    <p style='margin: 4px 0;'><strong>工号:</strong> {worker_info['工号']}</p>
                    <p style='margin: 4px 0;'><strong>年龄:</strong> {worker_info['年龄']}岁</p>
                    <p style='margin: 4px 0;'><strong>职位:</strong> {worker_info['职位']}</p>
                    <p style='margin: 4px 0;'><strong>所在区域:</strong> {worker_info['所在区域']}</p>
                    <p style='margin: 4px 0;'><strong>紧急联系人:</strong> {worker_info['紧急联系人']}</p>
                    <hr style='margin: 10px 0; border: none; border-top: 1px solid rgba(255,255,255,0.3);'>
                    <p style='margin: 4px 0;'><strong>当前风险值:</strong> <span style='color: #ffeb3b; font-weight: bold;'>{worker_info['风险值']:.1f}</span></p>
                    <p style='margin: 4px 0;'><strong>疲劳度:</strong> <span style='color: #ffeb3b; font-weight: bold;'>{worker_info['疲劳度']:.1f}</span></p>
                    <p style='margin: 4px 0;'><strong>注意力:</strong> <span style='color: #ffeb3b; font-weight: bold;'>{worker_info['注意力']:.1f}</span></p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 基础分析部分（去掉白框，放大字体）
        st.markdown("""
        <h3 style='color: #5a7fd6; margin: 25px 0 15px 0; font-size: 24px; font-weight: bold;'>基础分析</h3>
        """, unsafe_allow_html=True)

        # 三个分析标签
        tab_col1, tab_col2, tab_col3 = st.columns(3)

        if 'individual_analysis_tab' not in st.session_state:
            st.session_state.individual_analysis_tab = '心理负荷水平'

        with tab_col1:
            if st.button("心理负荷水平",
                         type="primary" if st.session_state.individual_analysis_tab == '心理负荷水平' else "secondary",
                         use_container_width=True, key="tab_mental"):
                st.session_state.individual_analysis_tab = '心理负荷水平'
                st.rerun()
        with tab_col2:
            if st.button("语音分析",
                         type="primary" if st.session_state.individual_analysis_tab == '语音分析' else "secondary",
                         use_container_width=True, key="tab_voice"):
                st.session_state.individual_analysis_tab = '语音分析'
                st.rerun()
        with tab_col3:
            if st.button("心电活动",
                         type="primary" if st.session_state.individual_analysis_tab == '心电活动' else "secondary",
                         use_container_width=True, key="tab_ecg"):
                st.session_state.individual_analysis_tab = '心电活动'
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # 根据选中的标签显示不同内容
        if st.session_state.individual_analysis_tab == '心理负荷水平':
            # 心理负荷水平折线图
            times = ['8:00', '10:00', '12:00', '14:00', '16:00', '18:00']

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=times, y=mental_levels,
                mode='lines+markers',
                name='心理负荷',
                line=dict(color='#ff9800', width=3),
                marker=dict(size=10, color='#ff9800'),
            ))

            # 添加水平参考线
            fig.add_hline(y=4, line_dash="dash", line_color="red",
                          annotation_text="急需干预", annotation_position="right")
            fig.add_hline(y=3, line_dash="dash", line_color="orange",
                          annotation_text="待干预", annotation_position="right")
            fig.add_hline(y=2, line_dash="dash", line_color="yellow",
                          annotation_text="较稳定", annotation_position="right")
            fig.add_hline(y=1, line_dash="dash", line_color="green",
                          annotation_text="稳定", annotation_position="right")

            fig.update_layout(
                height=350,
                yaxis=dict(range=[0, 5], title="负荷水平",
                           ticktext=['起始', '稳定', '较稳定', '待干预', '急需干预'],
                           tickvals=[0, 1, 2, 3, 4]),
                xaxis_title="时间",
                plot_bgcolor='white',
                paper_bgcolor='white',
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True, config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                           'autoScale2d', 'resetScale2d'],
                'displaylogo': False
            })

        elif st.session_state.individual_analysis_tab == '语音分析':
            st.markdown(f"""
            <div class="white-card">
                <h4 style='color: #5a7fd6; margin-bottom: 15px;'>语音情绪分析</h4>
                <p><strong>情绪状态:</strong> <span style='color: #ff9800;'>{emotion_status}</span></p>
                <p><strong>语速:</strong> {speech_rate}词/分钟</p>
                <p><strong>音量:</strong> {'偏高' if worker_hash % 2 == 0 else '正常'}</p>
                <p><strong>语调变化:</strong> {'频繁' if worker_hash % 3 == 0 else '稳定'}</p>
                <br>
                <p style='color: #666; font-size: 13px;'>📊 {'最近检测到工人语音中存在焦虑情绪，建议关注其工作状态。' if emotion_status == '焦虑' else '工人语音状态正常。'}</p>
            </div>
            """, unsafe_allow_html=True)

        else:  # 心电活动
            st.markdown(f"""
            <div class="white-card">
                <h4 style='color: #5a7fd6; margin-bottom: 15px;'>心电监测数据</h4>
                <p><strong>心率:</strong> <span style='color: {"#ff5722" if heart_rate > 90 else "#4caf50"};'>{heart_rate} bpm</span> {'(偏高)' if heart_rate > 90 else '(正常)'}</p>
                <p><strong>心率变异性:</strong> 正常</p>
                <p><strong>异常心律:</strong> 未检测到</p>
                <p><strong>疲劳度:</strong> <span style='color: #ff9800;'>{fatigue}</span></p>
                <br>
                <p style='color: #666; font-size: 13px;'>{'⚠️ 心率略高于正常范围，建议适当休息。' if heart_rate > 90 else '✅ 心电数据正常。'}</p>
            </div>
            """, unsafe_allow_html=True)

        # 智能分析部分（移到这里，去掉白框，放大字体）
        st.markdown("""
        <h3 style='color: #5a7fd6; margin: 30px 0 15px 0; font-size: 24px; font-weight: bold;'>智能分析</h3>
        <p style='color: #666; font-size: 15px; margin-bottom: 20px;'>实时风险构成分析</p>
        """, unsafe_allow_html=True)

        # 风险构成饼图
        risk_labels = ['生理', '行为', '环境', '文本']
        risk_colors = ['#4285f4', '#ff9800', '#ffca28', '#66bb6a']

        fig_pie = go.Figure(data=[go.Pie(
            labels=risk_labels,
            values=risk_values,
            hole=0.4,
            marker=dict(colors=risk_colors),
            textposition='inside',
            textinfo='label+percent',
            textfont=dict(size=14, color='white')
        )])

        fig_pie.update_layout(
            height=300,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(fig_pie, use_container_width=True, config={
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                       'resetScale2d'],
            'displaylogo': False
        })

        # 行为识别 / 状态识别标签
        tab_col1, tab_col2 = st.columns(2)

        if 'recognition_tab' not in st.session_state:
            st.session_state.recognition_tab = '行为识别'

        with tab_col1:
            if st.button("行为识别",
                         type="primary" if st.session_state.recognition_tab == '行为识别' else "secondary",
                         use_container_width=True, key="tab_behavior"):
                st.session_state.recognition_tab = '行为识别'
                st.rerun()
        with tab_col2:
            if st.button("状态识别",
                         type="primary" if st.session_state.recognition_tab == '状态识别' else "secondary",
                         use_container_width=True, key="tab_status"):
                st.session_state.recognition_tab = '状态识别'
                st.rerun()

        # 修改2: 监控视频区域已从这里移除 ← 原来在这里

    with col_right:
        # 进入干预措施按钮（移到右侧顶部）
        if st.button("🎯 进入干预措施", use_container_width=True, type="primary", key="goto_intervention"):
            st.session_state.current_page = '干预措施'
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # 两个预测卡片缩小到一半宽度，放在一排
        col_pred1, col_pred2 = st.columns(2)

        with col_pred1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px 15px; border-radius: 12px; text-align: center; 
                        color: white; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
                <div style='font-size: 11px; margin-bottom: 8px;'>预测16:00未系安全带概率</div>
                <div style='font-size: 42px; font-weight: bold; line-height: 1;'>{predict_prob}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col_pred2:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px 15px; border-radius: 12px; text-align: center; 
                        color: white; box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);'>
                <div style='font-size: 11px; margin-bottom: 8px;'>历史相似案例相似度匹配</div>
                <div style='font-size: 42px; font-weight: bold; line-height: 1;'>{similarity}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 日期查询功能
        st.markdown("""
        <h4 style='color: #5a7fd6; margin-bottom: 15px;'>📅 时间查询</h4>
        """, unsafe_allow_html=True)

        if 'individual_start_date' not in st.session_state:
            st.session_state.individual_start_date = datetime.now().date()
        if 'individual_end_date' not in st.session_state:
            st.session_state.individual_end_date = datetime.now().date()

        start_date = st.date_input("开始日期",
                                   value=st.session_state.individual_start_date,
                                   key="individual_start_input")

        end_date = st.date_input("结束日期",
                                 value=st.session_state.individual_end_date,
                                 key="individual_end_input")

        col_query, col_reset = st.columns(2)
        with col_query:
            if st.button("🔍 查询", use_container_width=True, key="query_individual"):
                st.session_state.individual_start_date = start_date
                st.session_state.individual_end_date = end_date
                days_diff = (end_date - start_date).days + 1
                st.success(f"✅ 查询时间段: {start_date} 至 {end_date}\n共 {days_diff} 天")
        with col_reset:
            if st.button("🔄 重置", use_container_width=True, key="reset_individual"):
                st.session_state.individual_start_date = datetime.now().date()
                st.session_state.individual_end_date = datetime.now().date()
                st.rerun()

        # 查询结果统计
        if st.session_state.individual_start_date and st.session_state.individual_end_date:
            days_diff = (st.session_state.individual_end_date - st.session_state.individual_start_date).days + 1

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <h4 style='color: #5a7fd6; margin-bottom: 15px;'>📊 统计数据</h4>
            """, unsafe_allow_html=True)

            # 根据查询时间段显示不同统计
            violation_count = np.random.randint(0, days_diff * 3)
            warning_count = np.random.randint(0, days_diff * 5)
            intervention_count = np.random.randint(0, days_diff * 2)

            st.markdown(f"""
            <div class="white-card">
                <p><strong>查询时间段:</strong> {days_diff} 天</p>
                <p><strong>违规次数:</strong> <span style='color: #f44336;'>{violation_count}</span></p>
                <p><strong>预警次数:</strong> <span style='color: #ff9800;'>{warning_count}</span></p>
                <p><strong>干预次数:</strong> <span style='color: #4caf50;'>{intervention_count}</span></p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 修改3: 监控视频区域移到这里（识别结果上方）← 移到这里
        st.markdown("""
        <div style='background: #f5f5f5; padding: 15px; border-radius: 10px; 
                    text-align: center; margin-bottom: 15px; position: relative;'>
            <div style='background: #333; color: white; padding: 8px; 
                        border-radius: 6px; font-size: 12px; margin-bottom: 8px;'>
                📹 2021-04-11 星期四 09:30:28
            </div>
            <div style='background: #e0e0e0; height: 200px; border-radius: 8px; 
                        display: flex; align-items: center; justify-content: center; color: #666;'>
                <div>
                    <div style='font-size: 50px; margin-bottom: 10px;'>📷</div>
                    <div style='font-size: 16px;'>监控画面</div>
                </div>
            </div>
            <div style='position: absolute; bottom: 25px; right: 25px; 
                        background: rgba(90, 127, 214, 0.9); color: white; 
                        padding: 8px 15px; border-radius: 8px; font-size: 12px;'>
                🔍 未检测到异常
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 识别结果
        st.markdown("""
        <h4 style='color: #5a7fd6; margin-bottom: 15px;'>🔍 识别结果</h4>
        """, unsafe_allow_html=True)

        # 识别结果详情
        if st.session_state.recognition_tab == '行为识别':
            helmet_ok = worker_hash % 5 != 0
            belt_ok = worker_hash % 3 != 0
            st.markdown(f"""
            <div class="white-card">
                <h4 style='color: #5a7fd6; margin-bottom: 12px;'>行为识别结果</h4>
                <p>{'✅' if helmet_ok else '❌'} <strong>安全帽佩戴:</strong> {'正确' if helmet_ok else '<span style="color: #f44336;">未检测到</span>'}</p>
                <p>{'✅' if belt_ok else '❌'} <strong>安全带系扣:</strong> {'正确' if belt_ok else '<span style="color: #f44336;">未检测到</span>'}</p>
                <p>✅ <strong>工作姿势:</strong> 正常</p>
                <p>⚠️ <strong>危险区域:</strong> <span style='color: #ff9800;'>{'接近' if worker_hash % 2 == 0 else '安全'}</span></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            expressions = ['中性', '微笑', '疲惫', '专注']
            expression = expressions[worker_hash % len(expressions)]
            st.markdown(f"""
            <div class="white-card">
                <h4 style='color: #5a7fd6; margin-bottom: 12px;'>状态识别结果</h4>
                <p>😐 <strong>面部表情:</strong> {expression}</p>
                <p>💪 <strong>肢体状态:</strong> 正常活动</p>
                <p>⚡ <strong>疲劳程度:</strong> <span style='color: #ff9800;'>{fatigue}</span></p>
                <p>👥 <strong>人员位置:</strong> 作业区域内</p>
            </div>
            """, unsafe_allow_html=True)

def render_training():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    # 修改1: 确保查询按钮和选择工号在同一水平线
    col_search1, col_search2, col_search3 = st.columns([2, 1, 7])
    with col_search1:
        worker_id = st.selectbox("选择工号",
                                 ["A12011", "A12012", "A12013", "A12014", "A12015"],
                                 key="search_worker",
                                 label_visibility="visible")
    with col_search2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)  # 添加间距对齐
        if st.button("🔍 查询", use_container_width=True):
            st.session_state.search_worker_id = worker_id
            st.toast(f"✅ 查询成功: {worker_id}", icon="🔍")

    st.markdown("<br>", unsafe_allow_html=True)

    # 修改2: 根据不同工号显示不同的课程学习结果
    courses_data = {
        "A12011": {
            "learning": [
                {"name": "起重机械与吊装作业安全要点", "progress": 59},
                {"name": "基坑开挖与支护安全警示案例", "progress": 42}
            ],
            "completed": [
                {"name": "建筑施工典型事故案例剖析", "progress": 100},
                {"name": "个人防护用品正确佩戴指南", "progress": 100}
            ],
            "radar": {'图纸': 30, '材料': 25, '法规': 15, '安全': 35, '验收': 20}
        },
        "A12012": {
            "learning": [
                {"name": "高处作业安全防护技术", "progress": 75},
                {"name": "脚手架搭设规范与要求", "progress": 38}
            ],
            "completed": [
                {"name": "消防安全知识培训", "progress": 100},
                {"name": "应急救援基础技能", "progress": 100}
            ],
            "radar": {'图纸': 35, '材料': 30, '法规': 25, '安全': 40, '验收': 28}
        },
        "A12013": {
            "learning": [
                {"name": "电气安全操作规程", "progress": 88},
                {"name": "机械设备安全使用指南", "progress": 52}
            ],
            "completed": [
                {"name": "建筑工地安全管理制度", "progress": 100},
                {"name": "职业健康防护知识", "progress": 100}
            ],
            "radar": {'图纸': 40, '材料': 35, '法规': 30, '安全': 45, '验收': 35}
        },
        "A12014": {
            "learning": [
                {"name": "混凝土施工质量控制", "progress": 45},
                {"name": "钢筋绑扎技术要点", "progress": 67}
            ],
            "completed": [
                {"name": "安全帽正确佩戴方法", "progress": 100},
                {"name": "高温作业防护措施", "progress": 100}
            ],
            "radar": {'图纸': 25, '材料': 20, '法规': 18, '安全': 30, '验收': 22}
        },
        "A12015": {
            "learning": [
                {"name": "塔吊操作安全规范", "progress": 92},
                {"name": "起重吊装作业安全", "progress": 78}
            ],
            "completed": [
                {"name": "特种作业人员安全培训", "progress": 100},
                {"name": "安全生产法律法规", "progress": 100}
            ],
            "radar": {'图纸': 45, '材料': 40, '法规': 35, '安全': 48, '验收': 40}
        }
    }

    current_worker = st.session_state.search_worker_id
    current_courses = courses_data.get(current_worker, courses_data["A12011"])

    col_left, col_middle, col_right = st.columns([3, 4, 3])

    with col_left:
        st.markdown("### 📚 课程管理")

        st.markdown(
            '<div style="background: #e3f2fd; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-weight: bold;">学习中</div>',
            unsafe_allow_html=True)

        for course in current_courses["learning"]:
            col_play, col_info = st.columns([1, 9])
            with col_play:
                # 修改4: 改用toast提示，不再是长长的竖条
                if st.button("▶", key=f"play_{course['name']}_{current_worker}", help="播放课程"):
                    st.toast(f"▶️ 正在播放: {course['name']}", icon="📺")
            with col_info:
                st.markdown(f"**{course['name']}**")
                st.caption(f"已学{course['progress']}/100节")
                st.progress(course['progress'] / 100)

        st.markdown(
            '<div style="background: #f0f0f0; padding: 10px; border-radius: 8px; margin: 20px 0 15px 0; font-weight: bold;">已学习</div>',
            unsafe_allow_html=True)

        for course in current_courses["completed"]:
            col_play, col_info = st.columns([1, 9])
            with col_play:
                if st.button("▶", key=f"play_{course['name']}_{current_worker}", help="播放课程"):
                    st.toast(f"▶️ 正在播放: {course['name']}", icon="📺")
            with col_info:
                st.markdown(f"**{course['name']}**")
                st.caption(f"已学{course['progress']}/100节")
                st.progress(course['progress'] / 100)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📝 安全信用记录")

        records = pd.DataFrame({
            '行为': ['规范行为', '隐患上报', '培训出勤', '活动参与', '违章行为'],
            '时间': ['2025-08-01 15:32', '2025-07-30 10:12', '2025-07-29 14:00',
                     '2025-07-29 15:00', '2025-07-27 17:04']
        })

        st.dataframe(records, use_container_width=True, hide_index=True, height=200)

    with col_middle:
        st.markdown("### 💡 安全知识问答")

        tab_col1, tab_col2, tab_col3 = st.columns(3)
        tabs = ['排行榜', '关键词', '时段表']

        for col, tab in zip([tab_col1, tab_col2, tab_col3], tabs):
            with col:
                if st.button(tab,
                             type="primary" if st.session_state.training_tab == tab else "secondary",
                             key=f"tab_{tab}",
                             use_container_width=True):
                    st.session_state.training_tab = tab
                    st.rerun()

        # 修改3: 完善三个标签页功能
        if st.session_state.training_tab == '排行榜':
            st.markdown("#### 📊 工人安全知识排行榜")

            ranking_data = pd.DataFrame({
                '排名': ['🥇', '🥈', '🥉', '4', '5', '6', '7', '8', '9', '10'],
                '工号': ['A12015', 'A12013', 'A12012', 'A12011', 'A12014',
                         'A12016', 'A12017', 'A12018', 'A12019', 'A12020'],
                '姓名': ['小E', '小C', '小B', '小A', '小D',
                         '小F', '小G', '小H', '小I', '小J'],
                '总分': [485, 472, 468, 445, 432, 428, 415, 402, 398, 385],
                '完成课程': [12, 11, 11, 10, 9, 9, 8, 8, 7, 7]
            })

            st.dataframe(ranking_data, use_container_width=True, hide_index=True, height=400)

            if current_worker in ranking_data['工号'].values:
                worker_rank = ranking_data[ranking_data['工号'] == current_worker].index[0] + 1
                worker_score = ranking_data[ranking_data['工号'] == current_worker]['总分'].values[0]
                st.info(f"🎯 当前查询工号 {current_worker} 排名: 第 {worker_rank} 名，总分: {worker_score} 分")

        elif st.session_state.training_tab == '关键词':
            st.markdown("#### 🔍 知识点雷达分析")

            # 修改3: 将雷达图移到关键词标签
            categories = ['图纸', '材料', '法规', '安全', '验收']
            current_values = list(current_courses["radar"].values())
            target_values = [40, 35, 30, 45, 35]

            fig = go.Figure()

            fig.add_trace(go.Scatterpolar(
                r=current_values + [current_values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(102, 126, 234, 0.3)',
                line=dict(color='#667eea', width=2),
                name='当前水平'
            ))

            fig.add_trace(go.Scatterpolar(
                r=target_values + [target_values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(255, 193, 7, 0.3)',
                line=dict(color='#ffc107', width=2),
                name='目标水平'
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
                showlegend=True,
                height=350,
                paper_bgcolor='white'
            )

            st.plotly_chart(fig, use_container_width=True, config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                           'autoScale2d', 'resetScale2d'],
                'displaylogo': False
            })

            st.markdown("**📌 薄弱知识点提示：**")
            weak_points = [k for k, v in current_courses["radar"].items() if v < 30]
            if weak_points:
                st.warning(f"需要加强学习：{', '.join(weak_points)}")
            else:
                st.success("各项知识点掌握良好！")

        else:  # 时段表
            st.markdown("#### 📅 学习时段统计")

            time_data = pd.DataFrame({
                '时段': ['08:00-10:00', '10:00-12:00', '14:00-16:00', '16:00-18:00', '20:00-22:00'],
                '学习次数': [15, 23, 18, 12, 8],
                '平均时长(分钟)': [45, 52, 38, 35, 28]
            })

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=time_data['时段'],
                y=time_data['学习次数'],
                name='学习次数',
                marker_color='#667eea',
                text=time_data['学习次数'],
                textposition='outside'
            ))

            fig.update_layout(
                height=300,
                yaxis=dict(range=[0, max(time_data['学习次数']) + 5]),
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )

            st.plotly_chart(fig, use_container_width=True, config={
                'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
                                           'autoScale2d', 'resetScale2d'],
                'displaylogo': False
            })

            st.markdown("**最活跃时段：** 10:00-12:00 ⏰")
            st.dataframe(time_data, use_container_width=True, hide_index=True)


    with col_right:
        st.markdown("### 📊 效果分析")

        metrics = ['如期完成率', '订单完整率', '质量合格率']
        values = [93.80, 99.90, 99.80]
        colors = ['#667eea', '#ffa500', '#ffc107']

        fig = go.Figure(data=[
            go.Bar(
                x=metrics, y=values,
                marker_color=colors,
                text=[f'{v}%' for v in values],
                textposition='outside',
            )
        ])

        fig.update_layout(
            height=300,
            yaxis=dict(range=[0, 110]),
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True, config={
            'modeBarButtonsToRemove': ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d',
                                       'resetScale2d'],
            'displaylogo': False
        })

        st.markdown("### 📢 最新消息")

        st.markdown("""
        <div class="white-card">
            <ol style='padding-left: 20px; line-height: 2.2;'>
                <li>《建筑工人三级安全教育视频》更新完成。</li>
                <li>小D进行了关键词为"安全防护"的安全知识问答。</li>
                <li>小C完成了《起重机械与吊装作业安全要点》课程的学习。</li>
                <li>小A对中园区隐患进行上报,安全信用分+5。</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)


def render_ai_assistant():
    st.markdown('<div class="main-header">筑安云脑安全氛围管理平台</div>', unsafe_allow_html=True)

    # 初始化会话管理
    if 'ai_sessions' not in st.session_state:
        st.session_state.ai_sessions = {
            'session_1': {
                'title': '新对话',
                'history': [],
                'timestamp': datetime.now()
            }
        }
    if 'current_session_id' not in st.session_state:
        st.session_state.current_session_id = 'session_1'
    if 'session_counter' not in st.session_state:
        st.session_state.session_counter = 1
    if 'input_counter' not in st.session_state:
        st.session_state.input_counter = 0

    # 创建左右布局
    col_sidebar, col_chat = st.columns([2, 8])

    # 左侧会话历史
    with col_sidebar:
        st.markdown("### 💬 对话历史")

        # 新建对话按钮
        if st.button("➕ 新建对话", use_container_width=True, type="primary"):
            st.session_state.session_counter += 1
            new_session_id = f'session_{st.session_state.session_counter}'
            st.session_state.ai_sessions[new_session_id] = {
                'title': f'新对话 {st.session_state.session_counter}',
                'history': [],
                'timestamp': datetime.now()
            }
            st.session_state.current_session_id = new_session_id
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # 显示会话列表
        for session_id in sorted(st.session_state.ai_sessions.keys(),
                                 key=lambda x: st.session_state.ai_sessions[x]['timestamp'],
                                 reverse=True):
            session = st.session_state.ai_sessions[session_id]
            is_current = session_id == st.session_state.current_session_id

            # 会话标题（如果有历史记录，显示第一条消息）
            if len(session['history']) > 0:
                display_title = session['history'][0]['content'][:20] + "..."
            else:
                display_title = session['title']

            # 会话按钮
            col_btn, col_del = st.columns([4, 1])
            with col_btn:
                if st.button(
                        f"{'📍 ' if is_current else '💬 '}{display_title}",
                        key=f"session_{session_id}",
                        use_container_width=True,
                        type="primary" if is_current else "secondary"
                ):
                    st.session_state.current_session_id = session_id
                    st.rerun()

            with col_del:
                if len(st.session_state.ai_sessions) > 1:  # 至少保留一个会话
                    if st.button("🗑️", key=f"del_{session_id}", help="删除对话"):
                        if session_id == st.session_state.current_session_id:
                            # 如果删除当前会话，切换到第一个会话
                            remaining = [sid for sid in st.session_state.ai_sessions.keys() if sid != session_id]
                            st.session_state.current_session_id = remaining[0]
                        del st.session_state.ai_sessions[session_id]
                        st.rerun()

    # 右侧聊天区域
    with col_chat:
        current_session = st.session_state.ai_sessions[st.session_state.current_session_id]

        # 欢迎区域（仅在空会话时显示）
        if len(current_session['history']) == 0:
            st.markdown("""
            <div style='text-align: center; padding: 60px 20px 40px 20px;'>
                <div style='font-size: 72px; margin-bottom: 20px;'>🤖</div>
                <h1 style='color: #5a7fd6; font-size: 36px; font-weight: bold; margin-bottom: 30px;'>
                    您好，我是您的智能AI助手小安，很高兴为您服务😍
                </h1>
            </div>
            """, unsafe_allow_html=True)

        # 聊天历史显示
        if len(current_session['history']) > 0:
            st.markdown("<div style='padding: 20px; max-height: 500px; overflow-y: auto;'>", unsafe_allow_html=True)

            for chat in current_session['history']:
                if chat['role'] == 'user':
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                color: white; padding: 15px 20px; border-radius: 18px; 
                                margin: 10px 0 10px auto; max-width: 70%; width: fit-content;
                                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
                                float: right; clear: both;'>
                        <div style='font-size: 14px;'>{chat['content']}</div>
                    </div>
                    <div style='clear: both;'></div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: rgba(255, 255, 255, 0.95); 
                                color: #333; padding: 15px 20px; border-radius: 18px; 
                                margin: 10px auto 10px 0; max-width: 70%; width: fit-content;
                                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                                border: 1px solid rgba(90, 127, 214, 0.2);
                                float: left; clear: both;'>
                        <div style='font-size: 14px; line-height: 1.6; white-space: pre-wrap;'>{chat['content']}</div>
                    </div>
                    <div style='clear: both;'></div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)


        # 底部输入区域（宽度扩大3倍）
        st.markdown("""
        <div style='border-top: 2px solid rgba(90, 113, 153, 0.1); padding-top: 5px; margin-top: 5px;'>
        </div>
        """, unsafe_allow_html=True)

        # 功能选项
        col_opt1, col_opt2, col_opt3 = st.columns([2, 2, 6])

        with col_opt1:
            deep_think = st.checkbox("🧠 深度思考", key=f"deep_think_{st.session_state.current_session_id}",
                                     help="启用深度分析模式")
        with col_opt2:
            web_search = st.checkbox("🌐 联网搜索", key=f"web_search_{st.session_state.current_session_id}",
                                     help="启用联网搜索（需配置API）")

        # 输入框（扩大宽度）
        col_input, col_send = st.columns([9, 1])

        with col_input:
            user_input = st.text_area(
                "",
                placeholder="请输入您的问题，例如：帮我分析工地安全风险...",
                key=f"ai_input_{st.session_state.current_session_id}_{st.session_state.input_counter}",  # ✅ 加上计数器
                label_visibility="collapsed",
                height=75
            )

        with col_send:
            send_button = st.button("Enter", key=f"send_{st.session_state.current_session_id}",
                                    use_container_width=True, type="primary", help="发送消息")

        # 处理发送消息
        if send_button and user_input.strip():
            # 添加用户消息
            current_session['history'].append({
                'role': 'user',
                'content': user_input
            })

            # 生成AI回复
            with st.spinner('AI正在思考中...'):
                ai_response = generate_ai_response(user_input, deep_think, web_search)

            current_session['history'].append({
                'role': 'assistant',
                'content': ai_response
            })

            # 更新会话标题
            if len(current_session['history']) == 2:
                current_session['title'] = user_input[:20] + "..."

            # ⭐️ 关键：增加计数器，下次rerun时key改变，输入框重建为空
            st.session_state.input_counter += 1

            st.rerun()

        # 清空当前对话按钮
        if len(current_session['history']) > 0:
            if st.button("🗑️ 清空当前对话", key=f"clear_{st.session_state.current_session_id}"):
                current_session['history'] = []
                current_session['title'] = '新对话'
                st.rerun()


def generate_ai_response(user_input, deep_think=False, web_search=False):
    """
    生成AI回复

    ⚠️ 重要说明：
    这里提供了接入真实AI API的框架代码。要使用真实AI功能，你需要：

    方案1: 使用Anthropic Claude API
    1. 安装: pip install anthropic
    2. 获取API密钥: https://console.anthropic.com/
    3. 取消注释下面的Claude API代码

    方案2: 使用OpenAI API
    1. 安装: pip install openai
    2. 获取API密钥: https://platform.openai.com/
    3. 使用OpenAI的代码替换

    当前使用的是增强的规则匹配系统作为fallback。
    """

    # ============ 真实AI API调用示例（需要取消注释并配置） ============

    # 方案1: Anthropic Claude API（推荐）
    # try:
    #     import anthropic
    #
    #     # ⚠️ 请替换为你的实际API密钥
    #     client = anthropic.Anthropic(api_key="your-api-key-here")
    #
    #     system_prompt = """你是筑安云脑安全氛围管理平台的AI助手"小安"。
    #     你的职责是帮助用户：
    #     1. 解答系统使用问题
    #     2. 提供安全管理建议
    #     3. 分析数据和生成报告
    #     4. 查询工人和项目信息
    #
    #     请用专业、友好的语气回答，并在适当时候提供具体的操作指导。
    #     """
    #
    #     message = client.messages.create(
    #         model="claude-3-5-sonnet-20241022",
    #         max_tokens=1024,
    #         system=system_prompt,
    #         messages=[
    #             {"role": "user", "content": user_input}
    #         ]
    #     )
    #
    #     response = message.content[0].text
    #
    #     # 添加模式标识
    #     if deep_think:
    #         response += "\n\n🧠 **深度思考模式已启用** - 已为您进行深入分析。"
    #     if web_search:
    #         response += "\n\n🌐 **联网搜索模式** - 请配置API以启用此功能。"
    #
    #     return response
    #
    # except Exception as e:
    #     # 如果API调用失败，使用fallback
    #     pass

    # 方案2: OpenAI API
    # try:
    #     import openai
    #
    #     openai.api_key = "your-openai-api-key-here"
    #
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[
    #             {"role": "system", "content": "你是筑安云脑的AI助手小安..."},
    #             {"role": "user", "content": user_input}
    #         ]
    #     )
    #
    #     return response.choices[0].message.content
    #
    # except Exception as e:
    #     pass

    # ============ Fallback: 增强的规则匹配系统 ============

    user_input_lower = user_input.lower()

    # 构建系统知识库
    knowledge_base = {
        '风险管理': {
            'keywords': ['风险', '危险', '安全', '隐患', '预警', '防护'],
            'response': """**🛡️ 安全风险管理方案**

基于您的咨询，我为您提供以下建议：

**1. 实时监控体系**
- 利用系统的实时预警功能，24小时监控工人状态
- 设置多级预警阈值，及时发现潜在风险
- 查看路径：工作台 → 实时预警 → 总体分析

**2. 风险评估方法**
- 个体风险：疲劳度、注意力、违规记录
- 环境风险：作业区域、天气条件、设备状态
- 群体风险：团队氛围、从众心理

**3. 预防性干预**
- 高风险工人：立即干预，调整岗位或强制休息
- 中风险工人：加强监控，提供安全培训
- 低风险工人：定期检查，保持良好状态

**4. 数据追踪**
- 建立工人安全档案
- 记录每次干预措施和效果
- 分析历史数据，优化管理策略

💡 建议操作：前往"实时预警"模块查看当前高风险人员名单"""
        },

        '工人管理': {
            'keywords': ['工人', '人员', '员工', '姓名', '工号', '查询'],
            'response': """**👷 工人信息管理系统**

系统提供全方位的工人管理功能：

**基础信息管理**
- 📋 基本资料：姓名、工号、年龄、职位、联系方式
- 🏗️ 工作信息：所在区域、班组、作业内容
- 📊 风险评估：实时风险值、疲劳度、注意力水平

**个体分析功能**
- 心理负荷监测：实时追踪工人心理压力
- 语音情绪分析：通过语音识别情绪状态
- 心电活动监测：监控生理健康指标
- 行为识别：检测安全装备佩戴情况

**智能预测**
- 违规行为预测：基于历史数据预测风险
- 相似案例匹配：参考类似情况的处理方案

**操作指引**
1. 搜索工人：在搜索框输入姓名或工号
2. 查看详情：点击"实时预警 > 个体分析"
3. 制定干预：前往"干预措施"模块"""
        },

        '干预措施': {
            'keywords': ['干预', '措施', '处理', '解决', '对策', '调整'],
            'response': """**🎯 智能干预系统使用指南**

**干预计划制定**

1. **自动生成计划**
   - AI分析工人风险因素
   - 提供个性化干预建议
   - 预测干预效果

2. **常用干预措施**
   - 🔴 高风险：强制休息、岗位调整、停工整改
   - 🟡 中风险：加强培训、增加监控、班组调整
   - 🟢 低风险：定期检查、安全提醒、技能提升

3. **智能排程优化**
   - 根据工人状态自动调整工作安排
   - 避免高风险时段安排危险作业
   - 优化人员配置，提高安全性

**干预效果追踪**
- 记录每次干预的时间、措施、效果
- 对比干预前后的数据变化
- 统计违规下降率、事故减少率

**操作步骤**
1. 选择需要干预的工人
2. 查看AI生成的分析报告
3. 制定或修改干预计划
4. 执行并跟踪效果

📊 数据显示：系统干预后，平均违规率下降63%"""
        },

        '进度管理': {
            'keywords': ['进度', '项目', '工程', '完成', '计划', '时间'],
            'response': """**📈 工程进度管理系统**

**多级项目管理**

**一级项目**（主体工程）
- 主体结构、地基处理、交通配套、土方工程
- 当前进度：65%
- 总工期：12个月，已完成8个月

**二级项目**（机电安装）
- 钢结构、电气、给排水、暖通工程
- 当前进度：72%
- 总工期：10个月，已完成6个月

**三级项目**（装饰装修）
- 装修、绿化、智能化、消防工程
- 当前进度：58%
- 总工期：15个月，已完成9个月

**四级项目**（收尾工程）
- 外墙、道路、围墙、标识标牌
- 当前进度：80%
- 总工期：8个月，已完成5个月

**进度查询功能**
- 按日期筛选：查看特定时间段的进度
- 按项目筛选：查看特定项目的详细情况
- 按工人筛选：查看特定工人的干预记录

**问题管理**
- 建材浪费：已解决23/52个问题（44%）
- 安全隐患：已解决46/62个问题（74%）

🔍 查询提示：输入日期或项目名称进行精确查找"""
        },

        '培训学习': {
            'keywords': ['培训', '学习', '课程', '教育', '考试', '知识'],
            'response': """**🎓 安全培训系统**

**在线课程学习**

**学习中课程**
- 起重机械与吊装作业安全要点
- 基坑开挖与支护安全警示案例
- （可随时暂停和继续学习）

**已完成课程**
- 建筑施工典型事故案例剖析 ✅
- 个人防护用品正确佩戴指南 ✅

**知识考核系统**
- 📊 排行榜：查看全员学习排名
- 🔍 关键词分析：掌握薄弱知识点
- 📅 时段表：了解最佳学习时间

**知识点雷达图**
评估五大维度：
- 图纸识读能力
- 材料认知水平
- 法规理解程度
- 安全意识强度
- 验收标准掌握

**学习激励**
- 安全信用积分制度
- 学习排行榜
- 课程完成奖励
- 优秀学员表彰

**效果分析**
- 如期完成率：93.80%
- 订单完整率：99.90%
- 质量合格率：99.80%

💡 开始学习：前往"安全培训"模块选择课程"""
        },

        '系统使用': {
            'keywords': ['帮助', '使用', '教程', '怎么用', '如何', '操作', '功能'],
            'response': """**📖 系统使用完全指南**

**六大核心模块**

**1. 📊 工作台**
- 功能：总览安全态势和关键指标
- 内容：今日进度、预警数、干预数、风险指数
- 特色：3D工地实时模拟图

**2. ⚠️ 实时预警**
- 总体分析：查看未来7天风险趋势
- 个体分析：深入了解单个工人状态
- 功能：风险预测、智能分析、日期筛选

**3. 🎯 干预措施**
- 功能：制定和执行安全干预计划
- 特色：AI智能分析、排程优化
- 记录：干预计划、干预记录

**4. 📈 进度管理**
- 功能：跟踪项目进度和问题解决
- 分级：一级到四级项目管理
- 查询：按日期、项目、工人筛选

**5. 🎓 安全培训**
- 功能：在线学习和知识考核
- 内容：视频课程、知识问答、排行榜
- 分析：学习效果、知识雷达图

**6. 🤖 AI助手**（当前模块）
- 功能：智能问答和操作指导
- 特色：对话历史、深度思考、联网搜索

**快速开始**
1. 左侧导航栏选择功能模块
2. 使用搜索功能快速查找信息
3. 遇到问题随时问我！

**常见操作**
- 搜索工人：输入姓名或工号
- 查看风险：进入实时预警模块
- 制定干预：选择工人后进入干预措施
- 查询进度：在进度管理中按条件筛选

❓ 有任何疑问，请随时向我提问！"""
        },

        '数据分析': {
            'keywords': ['数据', '统计', '分析', '报告', '趋势', '图表'],
            'response': """**📊 数据分析与报告系统**

**实时数据监控**

**关键指标**
- 今日预警个数：47人
- 今日干预个数：34人
- 全局风险指数：52
- 今日工程进度：65%

**趋势分析**
- 未来7天风险趋势预测
- 关键风险节点识别
- 历史数据对比

**分级统计**
- L1（安全级）：稳定51.2%，不稳定15.7%
- L2（低危级）：稳定14.6%，不稳定5.1%
- L3（高危级）：稳定7.0%，不稳定6.4%

**效果评估**
- 违规下降率：63%
- 冲突减少率：45%
- 疲劳事故下降：54%

**可视化报表**
- 📈 折线图：显示风险变化趋势
- 📊 柱状图：对比不同指标
- 🥧 饼图：展示构成比例
- 🎯 雷达图：多维度能力评估

**导出功能**
- 生成PDF报告
- 导出Excel数据
- 分享数据看板

💻 查看详细数据：各模块均提供专业图表分析"""
        },

        '预测功能': {
            'keywords': ['预测', '预警', '预判', '未来', '可能', '概率'],
            'response': """**🔮 AI智能预测系统**

**违规行为预测**
- 基于历史数据和当前状态
- 预测未来时段的违规概率
- 示例：预测16:00未系安全带概率75%

**风险趋势预测**
- 未来7天风险值走势
- 识别高风险时间节点
- 提前安排预防措施

**相似案例匹配**
- 在历史数据库中搜索相似情况
- 相似度匹配度：85%
- 参考成功的干预方案

**预测依据**
1. **生理数据**：疲劳度、心率、睡眠质量
2. **行为数据**：历史违规记录、工作习惯
3. **环境数据**：天气、作业难度、时间段
4. **社交数据**：班组氛围、人际关系

**预测准确率**
- 短期预测（1-3小时）：92%
- 中期预测（1天）：85%
- 长期预测（7天）：78%

**应用场景**
- 提前安排休息时间
- 调整高风险作业计划
- 优化人员配置
- 准备应急预案

🎯 使用建议：结合实际情况，预测仅供参考"""
        }
    }

    # 智能匹配最相关的回复
    best_match = None
    max_score = 0

    for category, data in knowledge_base.items():
        score = sum(1 for keyword in data['keywords'] if keyword in user_input_lower)
        if score > max_score:
            max_score = score
            best_match = data['response']

    # 如果找到匹配
    if best_match and max_score > 0:
        response = best_match
    else:
        # 默认回复
        response = f"""**💬 关于「{user_input}」**

感谢您的咨询！作为筑安云脑的AI助手，我可以帮您：

**🔍 信息查询**
- 查询工人信息和风险状态
- 查看项目进度和完成情况
- 统计安全数据和效果分析

**📋 操作指导**
- 如何使用各个功能模块
- 如何制定干预计划
- 如何查看和导出报告

**💡 专业建议**
- 安全风险管理方案
- 人员配置优化建议
- 应急处理措施

**🎯 常见问题**
您可以尝试询问：
- "如何查看高风险工人？"
- "怎样制定干预计划？"
- "项目进度如何管理？"
- "如何进行安全培训？"
- "系统有哪些功能？"

或者告诉我您具体遇到的问题，我会尽力帮您解决！"""

    # 添加模式标识
    if deep_think:
        response += "\n\n---\n🧠 **深度思考模式已启用**\n\n我已为您进行了更深入的分析，考虑了多个相关因素、历史数据和最佳实践。如需更详细的分析，请告诉我具体需求。"

    if web_search:
        response += "\n\n---\n🌐 **联网搜索模式**\n\n⚠️ 注意：联网搜索功能需要配置真实的AI API（如Claude API或OpenAI API）。\n\n**配置方法：**\n1. 在代码中取消注释API调用部分\n2. 添加您的API密钥\n3. 重启应用\n\n当前使用的是本地知识库匹配系统。"

    return response


def render_settings():
    """渲染设置页面 - 现代化设置界面"""
    st.markdown('<div class="main-header">系统设置</div>', unsafe_allow_html=True)

    # 创建左右布局：左侧分类菜单，右侧设置详情
    col_menu, col_content = st.columns([2, 8])

    # 左侧设置分类菜单
    with col_menu:
        # 设置分类列表（带图标）
        categories = [
            ('🎨 通用设置', '通用设置'),
            ('👤 账户设置', '账户设置'),
            ('📊 显示设置', '显示设置'),
            ('⚠️ 安全设置', '安全设置'),
            ('💾 数据管理', '数据管理'),
            ('🔔 通知设置', '通知设置'),
            ('ℹ️ 关于系统', '关于系统')
        ]

        for label, category in categories:
            # 使用streamlit的按钮
            is_active = st.session_state.settings_category == category

            if st.button(label, key=f"cat_{category}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.settings_category = category
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # 右侧设置详情
    with col_content:
        # 根据选中的分类显示不同的设置内容
        if st.session_state.settings_category == '通用设置':
            render_general_settings()
        elif st.session_state.settings_category == '账户设置':
            render_account_settings()
        elif st.session_state.settings_category == '显示设置':
            render_display_settings()
        elif st.session_state.settings_category == '安全设置':
            render_security_settings()
        elif st.session_state.settings_category == '数据管理':
            render_data_settings()
        elif st.session_state.settings_category == '通知设置':
            render_notification_settings()
        elif st.session_state.settings_category == '关于系统':
            render_about_settings()


def render_general_settings():
    """通用设置"""
    st.markdown("### 🎨 通用设置")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown("#### 界面语言")
        language = st.selectbox(
            "",
            ["简体中文", "繁体中文", "English"],
            index=["简体中文", "繁体中文", "English"].index(st.session_state.language),
            key="language_select",
            label_visibility="collapsed"
        )
        if language != st.session_state.language:
            st.session_state.language = language
            st.success(f"✅ 语言已切换为: {language}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 主题模式")
        theme = st.radio(
            "",
            ["浅色模式", "深色模式", "自动切换"],
            index=["浅色模式", "深色模式", "自动切换"].index(st.session_state.theme_mode),
            horizontal=True,
            key="theme_select",
            label_visibility="collapsed"
        )
        if theme != st.session_state.theme_mode:
            st.session_state.theme_mode = theme
            st.success(f"✅ 主题已切换为: {theme}")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 自动刷新")
        auto_refresh = st.toggle(
            "启用自动刷新数据",
            value=st.session_state.auto_refresh,
            key="auto_refresh_toggle"
        )
        if auto_refresh != st.session_state.auto_refresh:
            st.session_state.auto_refresh = auto_refresh

        if auto_refresh:
            interval = st.slider(
                "刷新间隔（秒）",
                min_value=10,
                max_value=300,
                value=st.session_state.refresh_interval,
                step=10,
                key="refresh_interval_slider"
            )
            if interval != st.session_state.refresh_interval:
                st.session_state.refresh_interval = interval
                st.info(f"数据将每 {interval} 秒自动刷新")


def render_account_settings():
    """账户设置"""
    st.markdown("### 👤 账户设置")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 用户信息")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("用户名", value="管理员", key="username_input")
        st.text_input("邮箱", value="admin@zhuanyun.com", key="email_input")
    with col2:
        st.text_input("手机号", value="138****8888", key="phone_input")
        st.text_input("部门", value="安全管理部", key="department_input")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 修改密码")
    st.text_input("当前密码", type="password", key="current_password")
    st.text_input("新密码", type="password", key="new_password")
    st.text_input("确认新密码", type="password", key="confirm_password")

    if st.button("💾 保存修改", type="primary"):
        st.success("✅ 账户信息已更新")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("#### 安全选项")
    st.toggle("启用双因素认证", value=False, key="2fa_toggle")
    st.toggle("登录通知", value=True, key="login_notification")


def render_display_settings():
    """显示设置"""
    st.markdown("### 📊 显示设置")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 图表设置")
    st.toggle("显示图表动画效果", value=True, key="chart_animation")
    st.toggle("显示数据标签", value=True, key="show_labels")
    st.selectbox("默认图表类型", ["折线图", "柱状图", "饼图", "雷达图"], key="default_chart")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 3D工地模拟图设置")
    st.toggle("显示工人标记", value=True, key="show_worker_markers")
    st.toggle("显示建筑物标签", value=True, key="show_building_labels")
    st.slider("默认视角缩放", 0.5, 3.0, 1.6, 0.1, key="default_zoom")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 表格设置")
    st.number_input("每页显示行数", min_value=10, max_value=100, value=20, step=10, key="rows_per_page")
    st.toggle("启用表格排序", value=True, key="enable_sorting")
    st.toggle("启用表格筛选", value=True, key="enable_filtering")


def render_security_settings():
    """安全设置"""
    st.markdown("### ⚠️ 安全设置")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 风险等级阈值设置")
    st.caption("设置不同风险等级的阈值范围")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**L1 安全级**")
        l1_threshold = st.slider(
            "风险值上限",
            0, 100, st.session_state.risk_threshold_l1,
            key="l1_slider",
            help="低于此值为L1级别"
        )
        st.session_state.risk_threshold_l1 = l1_threshold
        st.success(f"L1: 0-{l1_threshold}")

    with col2:
        st.markdown("**L2 低危级**")
        l2_threshold = st.slider(
            "风险值上限",
            st.session_state.risk_threshold_l1, 100,
            st.session_state.risk_threshold_l2,
            key="l2_slider",
            help=f"{st.session_state.risk_threshold_l1}-此值为L2级别"
        )
        st.session_state.risk_threshold_l2 = l2_threshold
        st.warning(f"L2: {l1_threshold}-{l2_threshold}")

    with col3:
        st.markdown("**L3 高危级**")
        l3_threshold = st.slider(
            "风险值上限",
            st.session_state.risk_threshold_l2, 100,
            st.session_state.risk_threshold_l3,
            key="l3_slider",
            help=f"{st.session_state.risk_threshold_l2}-100为L3级别"
        )
        st.session_state.risk_threshold_l3 = l3_threshold
        st.error(f"L3: {l2_threshold}-100")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 预警设置")
    st.toggle("启用实时预警", value=True, key="enable_realtime_alert")
    st.toggle("高风险工人自动通知", value=True, key="auto_notify_high_risk")
    st.number_input("连续预警次数触发强制干预", 1, 10, 3, key="alert_trigger_count")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 数据保留设置")
    st.selectbox("预警记录保留时长", ["7天", "30天", "90天", "永久"], index=2, key="alert_retention")
    st.selectbox("干预记录保留时长", ["30天", "90天", "180天", "永久"], index=3, key="intervention_retention")


def render_data_settings():
    """数据管理设置"""
    st.markdown("### 💾 数据管理")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 数据导出")
    st.caption("导出系统数据用于备份或分析")

    col1, col2 = st.columns(2)
    with col1:
        export_type = st.selectbox("选择数据类型", [
            "工人信息", "预警记录", "干预记录", "进度数据", "培训记录", "全部数据"
        ], key="export_type")
    with col2:
        export_format = st.selectbox("导出格式", ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"], key="export_format")

    if st.button("📥 导出数据", type="primary"):
        st.success(f"✅ {export_type} 已导出为 {export_format} 格式")
        st.info("💡 提示：数据文件已保存到系统默认下载目录")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 数据备份")
    st.toggle("启用自动备份", value=True, key="auto_backup")
    st.selectbox("备份频率", ["每天", "每周", "每月"], key="backup_frequency")
    st.number_input("保留备份数量", 1, 30, 7, key="backup_count")

    if st.button("🔄 立即备份", type="secondary"):
        with st.spinner("正在备份数据..."):
            import time
            time.sleep(1)
        st.success("✅ 数据备份完成！")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 数据清理")
    st.warning("⚠️ 警告：数据清理操作不可逆，请谨慎操作！")

    if st.button("🗑️ 清除历史预警记录（7天前）", type="secondary"):
        if st.button("⚠️ 确认清除", type="secondary", key="confirm_clear"):
            st.success("✅ 历史预警记录已清除")

    if st.button("🔄 重置所有设置为默认值", type="secondary"):
        if st.button("⚠️ 确认重置", type="secondary", key="confirm_reset"):
            st.session_state.risk_threshold_l1 = 30
            st.session_state.risk_threshold_l2 = 60
            st.session_state.risk_threshold_l3 = 80
            st.success("✅ 设置已重置为默认值")
            st.rerun()


def render_notification_settings():
    """通知设置"""
    st.markdown("### 🔔 通知设置")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 推送通知")
    notification_enabled = st.toggle(
        "启用系统通知",
        value=st.session_state.notification_enabled,
        key="notification_main_toggle"
    )
    st.session_state.notification_enabled = notification_enabled

    if notification_enabled:
        st.markdown("**选择通知类型**")
        st.checkbox("高风险工人预警", value=True, key="notify_high_risk")
        st.checkbox("干预措施提醒", value=True, key="notify_intervention")
        st.checkbox("项目进度更新", value=True, key="notify_progress")
        st.checkbox("培训任务提醒", value=False, key="notify_training")
        st.checkbox("系统更新通知", value=False, key="notify_system")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 通知方式")
        st.checkbox("浏览器推送", value=True, key="browser_notification")
        st.checkbox("邮件通知", value=True, key="email_notification")
        st.checkbox("短信通知（仅紧急情况）", value=False, key="sms_notification")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("#### 免打扰模式")
        enable_dnd = st.toggle("启用免打扰时段", value=False, key="enable_dnd")
        if enable_dnd:
            col1, col2 = st.columns(2)
            with col1:
                st.time_input("开始时间", key="dnd_start")
            with col2:
                st.time_input("结束时间", key="dnd_end")
    else:
        st.info("💡 系统通知已关闭，您将不会收到任何推送消息")


def render_about_settings():
    """关于系统"""
    st.markdown("### ℹ️ 关于系统")
    st.markdown("<br>", unsafe_allow_html=True)

    # 系统信息卡片
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 40px 30px; border-radius: 16px; color: white; text-align: center;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3); margin-bottom: 30px;'>
        <div style='font-size: 60px; margin-bottom: 15px;'>🏗️</div>
        <h2 style='margin: 10px 0; font-size: 28px;'>筑安云脑安全氛围管理平台</h2>
        <p style='font-size: 14px; opacity: 0.9; margin-top: 10px;'>Construction Safety Management System</p>
        <div style='margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.3);'>
            <p style='font-size: 16px;'><strong>版本号:</strong> v2.5.1</p>
            <p style='font-size: 14px; margin-top: 8px; opacity: 0.9;'>最后更新: 2025年10月19日</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 系统详情
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 系统信息")
        st.markdown("""
        - **开发团队**: 筑安云脑研发中心
        - **技术栈**: Python + Streamlit
        - **数据库**: PostgreSQL
        - **AI引擎**: Claude API
        - **部署环境**: Cloud Server
        """)

    with col2:
        st.markdown("#### 📞 联系我们")
        st.markdown("""
        - **客服热线**: 400-888-9999
        - **技术支持**: support@zhuanyun.com
        - **商务合作**: business@zhuanyun.com
        - **官方网站**: www.zhuanyun.com
        - **工作时间**: 周一至周五 9:00-18:00
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 🔄 检查更新")
    if st.button("检查系统更新", type="primary"):
        with st.spinner("正在检查更新..."):
            import time
            time.sleep(1.5)
        st.success("✅ 当前已是最新版本 v2.5.1")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### 📄 法律信息")
    with st.expander("用户协议"):
        st.markdown("""
        欢迎使用筑安云脑安全氛围管理平台。使用本系统即表示您同意以下条款...

        1. 用户需妥善保管账户信息
        2. 禁止非法使用系统数据
        3. 遵守相关法律法规
        ...
        """)

    with st.expander("隐私政策"):
        st.markdown("""
        我们重视您的隐私保护，本政策说明我们如何收集、使用和保护您的信息...

        1. 信息收集：工人基本信息、作业数据等
        2. 信息使用：安全分析、风险预警等
        3. 信息保护：加密存储、权限控制
        ...
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 13px; padding: 20px 0;'>
        © 2025 筑安云脑科技有限公司 版权所有<br>
        Built with ❤️ by ZhuanYun Team
    </div>
    """, unsafe_allow_html=True)


def render_feedback():
    """渲染建议反馈页面"""
    st.markdown('<div class="main-header">意见反馈与建议</div>', unsafe_allow_html=True)

    # 创建两栏布局
    col_form, col_history = st.columns([6, 4])

    with col_form:
        # 反馈表单
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(248,250,252,0.97) 100%); 
                    padding: 30px; border-radius: 14px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
                    backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.9);'>
            <h3 style='color: #5a7fd6; margin-bottom: 20px;'>📝 提交您的建议</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: -20px;'>", unsafe_allow_html=True)

        # 反馈类型
        st.markdown("#### 反馈类型")
        feedback_type = st.selectbox(
            "",
            ["功能建议", "Bug反馈", "性能问题", "界面优化", "数据准确性", "其他"],
            key="feedback_type",
            label_visibility="collapsed"
        )

        # 优先级
        st.markdown("#### 优先级")
        priority = st.radio(
            "",
            ["低", "中", "高", "紧急"],
            horizontal=True,
            key="feedback_priority",
            label_visibility="collapsed"
        )

        # 反馈标题
        st.markdown("#### 问题/建议标题")
        title = st.text_input(
            "",
            placeholder="请简要描述您的问题或建议（必填）",
            key="feedback_title",
            label_visibility="collapsed"
        )

        # 详细描述
        st.markdown("#### 详细描述")
        description = st.text_area(
            "",
            placeholder="请详细描述您遇到的问题、改进建议或想法...\n\n例如：\n- 问题出现的具体步骤\n- 期望的功能表现\n- 改进建议的详细说明",
            height=200,
            key="feedback_description",
            label_visibility="collapsed"
        )

        # 联系方式
        st.markdown("#### 联系方式（可选）")
        col1, col2 = st.columns(2)
        with col1:
            contact_name = st.text_input("姓名", key="feedback_name")
        with col2:
            contact_email = st.text_input("邮箱", key="feedback_email")

        # 附件上传
        st.markdown("#### 附件（可选）")
        uploaded_file = st.file_uploader(
            "上传截图或相关文件",
            type=["png", "jpg", "jpeg", "pdf", "doc", "docx"],
            key="feedback_attachment",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 提交按钮
        col_submit, col_reset = st.columns([1, 1])
        with col_submit:
            if st.button("📤 提交反馈", type="primary", use_container_width=True):
                if not title or not description:
                    st.error("❌ 请填写标题和详细描述")
                else:
                    # 保存反馈到session state
                    if 'feedback_list' not in st.session_state:
                        st.session_state.feedback_list = []

                    feedback_data = {
                        'id': len(st.session_state.feedback_list) + 1,
                        'type': feedback_type,
                        'priority': priority,
                        'title': title,
                        'description': description,
                        'name': contact_name if contact_name else "匿名用户",
                        'email': contact_email,
                        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': '待处理',
                        'has_attachment': uploaded_file is not None
                    }

                    st.session_state.feedback_list.append(feedback_data)
                    st.success("✅ 反馈提交成功！我们会尽快处理您的反馈。")

                    # 清空表单
                    st.session_state.feedback_title = ""
                    st.session_state.feedback_description = ""
                    st.rerun()

        with col_reset:
            if st.button("🔄 重置表单", use_container_width=True):
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_history:
        # 反馈历史记录
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255,255,255,0.97) 0%, rgba(248,250,252,0.97) 100%); 
                    padding: 25px; border-radius: 14px; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
                    backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.9);'>
            <h3 style='color: #5a7fd6; margin-bottom: 20px;'>📋 我的反馈历史</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 显示反馈列表
        if 'feedback_list' not in st.session_state or len(st.session_state.feedback_list) == 0:
            st.info("💡 暂无反馈记录，提交您的第一条反馈吧！")
        else:
            # 按时间倒序显示
            for feedback in reversed(st.session_state.feedback_list):
                # 优先级颜色
                priority_colors = {
                    '低': '#4caf50',
                    '中': '#ff9800',
                    '高': '#ff5722',
                    '紧急': '#f44336'
                }
                priority_color = priority_colors[feedback['priority']]

                # 状态颜色
                status_colors = {
                    '待处理': '#9e9e9e',
                    '处理中': '#2196f3',
                    '已完成': '#4caf50',
                    '已关闭': '#607d8b'
                }
                status_color = status_colors.get(feedback['status'], '#9e9e9e')

                with st.expander(f"#{feedback['id']} - {feedback['title']}", expanded=False):
                    st.markdown(f"""
                    <div style='padding: 10px;'>
                        <p><strong>类型:</strong> {feedback['type']}</p>
                        <p><strong>优先级:</strong> <span style='color: {priority_color}; font-weight: bold;'>{feedback['priority']}</span></p>
                        <p><strong>状态:</strong> <span style='color: {status_color}; font-weight: bold;'>{feedback['status']}</span></p>
                        <p><strong>提交时间:</strong> {feedback['time']}</p>
                        <p><strong>提交人:</strong> {feedback['name']}</p>
                        <hr style='margin: 10px 0; border: none; border-top: 1px solid #eee;'>
                        <p><strong>详细描述:</strong></p>
                        <p style='color: #555; line-height: 1.6;'>{feedback['description']}</p>
                        {f"<p>📎 <em>包含附件</em></p>" if feedback['has_attachment'] else ""}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # 快速联系方式
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 12px; color: white; margin-top: 20px;'>
            <h4 style='margin: 0 0 15px 0;'>📞 快速联系</h4>
            <p style='margin: 5px 0; font-size: 14px;'>客服热线: 400-888-9999</p>
            <p style='margin: 5px 0; font-size: 14px;'>技术支持: support@zhuanyun.com</p>
            <p style='margin: 5px 0; font-size: 14px;'>工作时间: 周一至周五 9:00-18:00</p>
        </div>
        """, unsafe_allow_html=True)

        # 常见问题
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ❓ 常见问题")

        with st.expander("如何修改密码？"):
            st.markdown("进入 **设置 > 账户设置**，在修改密码区域输入当前密码和新密码即可。")

        with st.expander("如何导出数据？"):
            st.markdown("进入 **设置 > 数据管理**，选择需要导出的数据类型和格式，点击导出按钮。")

        with st.expander("系统支持哪些浏览器？"):
            st.markdown("推荐使用 Chrome、Edge、Firefox 等现代浏览器的最新版本。")

        with st.expander("如何联系技术支持？"):
            st.markdown("可以通过本页面提交反馈，或直接拨打客服热线 400-888-9999。")

def render_calendar(highlighted_dates=None):
    if highlighted_dates is None:
        highlighted_dates = [1]

    current_date = 1

    calendar_html = """
    <style>
        .calendar {
            background: rgba(255, 255, 255, 0.97);
            padding: 15px;
            border-radius: 14px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            border: 1px solid rgba(255, 255, 255, 0.9);
        }
        .calendar-header {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
            margin-bottom: 10px;
            font-weight: bold;
            text-align: center;
            color: #5a7199;
        }
        .calendar-days {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
        }
        .calendar-day {
            padding: 10px 5px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .calendar-day:hover {
            background: #dfe7f2;
        }
        .today {
            background: #5a7fd6;
            color: white;
            font-weight: bold;
        }
        .highlighted {
            background: #b8cde6;
            font-weight: 600;
            color: #333;
        }
    </style>
    <div class="calendar">
        <div class="calendar-header">
            <div>日</div><div>一</div><div>二</div><div>三</div>
            <div>四</div><div>五</div><div>六</div>
        </div>
        <div class="calendar-days">
    """

    for day in range(1, 32):
        is_today = day == current_date
        is_highlighted = day in highlighted_dates
        class_name = "today" if is_today else ("highlighted" if is_highlighted else "")
        calendar_html += f'<div class="calendar-day {class_name}">{day}</div>'

    calendar_html += "</div></div>"
    st.markdown(calendar_html, unsafe_allow_html=True)


def main():
    render_sidebar()

    if st.session_state.current_page == '工作台':
        render_dashboard()
    elif st.session_state.current_page == '总体分析':
        render_alerts()          # 复用原来的实时预警总览
    elif st.session_state.current_page == '个体分析':
        render_individual_analysis()  # 新页面（见下）
    elif st.session_state.current_page == '干预措施':
        render_interventions()
    elif st.session_state.current_page == '进度管理':
        render_progress()
    elif st.session_state.current_page == '安全培训':
        render_training()
    elif st.session_state.current_page == '智能AI助手':
        render_ai_assistant()
    elif st.session_state.current_page == '设置':
        render_settings()
    elif st.session_state.current_page == '建议反馈':
        render_feedback()


if __name__ == "__main__":
    main()
