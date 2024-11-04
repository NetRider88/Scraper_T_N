import streamlit as st
import pandas as pd
import time
from scraping.noon_scraper import scrape_noon_food
from scraping.talabat_scraper import scrape_talabat
from scraping.area_data import get_all_uae_areas
import logging
import io
from datetime import datetime
import random
from scraping.area_mapping import AreaMapping

# Matrix-style CSS
MATRIX_STYLE = """
<style>
    .matrix-terminal {
        background-color: #000000;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
        padding: 20px;
        border-radius: 5px;
        border: 2px solid #00ff00;
        box-shadow: 0 0 20px #00ff00;
        height: 500px;
        overflow-y: auto;
        margin-bottom: 20px;
        white-space: pre-line;
        position: relative;
    }
    .matrix-log {
        margin: 4px 0;
        padding: 4px;
        animation: fadeIn 0.3s ease-out;
        text-shadow: 0 0 5px #00ff00;
    }
    .matrix-glow {
        color: #00ff00;
        text-shadow: 0 0 10px #00ff00;
        margin-right: 8px;
        font-weight: bold;
    }
    .success { 
        color: #00ff00; 
        text-shadow: 0 0 8px #00ff00;
    }
    .error { 
        color: #ff0000; 
        text-shadow: 0 0 8px #ff0000;
    }
    .warning { 
        color: #ffff00; 
        text-shadow: 0 0 8px #ffff00;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .matrix-terminal::-webkit-scrollbar {
        width: 10px;
        background: #000000;
    }
    .matrix-terminal::-webkit-scrollbar-thumb {
        background: #00ff00;
        border-radius: 5px;
    }
</style>
"""

MATRIX_RAIN_SCRIPT = """
<script>
    function createMatrixRain() {
        const container = document.querySelector('.matrix-terminal');
        const rain = document.createElement('div');
        rain.className = 'matrix-rain';
        container.appendChild(rain);

        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
        const columns = Math.floor(container.offsetWidth / 20);

        for (let i = 0; i < columns; i++) {
            const drop = document.createElement('div');
            drop.className = 'matrix-drop';
            drop.style.left = `${i * 20}px`;
            drop.style.animationDuration = `${Math.random() * 2 + 1}s`;
            drop.style.animationDelay = `${Math.random() * 2}s`;
            drop.textContent = chars[Math.floor(Math.random() * chars.length)];
            rain.appendChild(drop);
        }

        setInterval(() => {
            document.querySelectorAll('.matrix-drop').forEach(drop => {
                drop.textContent = chars[Math.floor(Math.random() * chars.length)];
            });
        }, 100);
    }

    // Run after a short delay to ensure the terminal is rendered
    setTimeout(createMatrixRain, 500);
</script>
"""

class MatrixStreamlitHandler(logging.Handler):
    def __init__(self, terminal_container):
        super().__init__()
        self.terminal_container = terminal_container
        self.logs = []
        self.matrix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
        
    def get_matrix_effect(self):
        return ''.join(random.choice(self.matrix_chars) for _ in range(4))
        
    def get_log_style(self, record):
        if "Scraped restaurant:" in record.msg:
            return "success"
        elif "ERROR" in record.levelname:
            return "error"
        elif "WARNING" in record.levelname:
            return "warning"
        return ""
        
    def emit(self, record):
        try:
            msg = self.format(record)
            matrix_prefix = self.get_matrix_effect()
            log_style = self.get_log_style(record)
            
            log_entry = (
                f'<div class="matrix-log {log_style}">'
                f'<span class="matrix-glow">[{matrix_prefix}]</span> {msg}'
                f'</div>'
            )
            
            self.logs.append(log_entry)
            
            log_html = f"""
            <div class="matrix-terminal">
                {''.join(self.logs)}
            </div>
            """
            
            self.terminal_container.markdown(log_html, unsafe_allow_html=True)
            
        except Exception as e:
            print(f"Error in emit: {str(e)}")
            self.handleError(record)

    def log_with_data(self, level, msg, data=None):
        record = logging.LogRecord(
            name=self.name,
            level=level,
            pathname='',
            lineno=0,
            msg=msg,
            args=(),
            exc_info=None
        )
        if data is not None:
            record.data = data
        return record

def setup_logger(terminal_container):
    logger = logging.getLogger('matrix_logger')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    matrix_handler = MatrixStreamlitHandler(terminal_container)
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    matrix_handler.setFormatter(formatter)
    logger.addHandler(matrix_handler)
    
    # Add the styles to the page once
    st.markdown(MATRIX_STYLE, unsafe_allow_html=True)
    
    return logger

def matrix_loading_effect(message, duration=0.05):
    """Creates a Matrix-style loading effect"""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
    msg_placeholder = st.empty()
    
    for _ in range(10):  # Number of animation frames
        random_chars = ''.join(random.choice(chars) for _ in range(len(message)))
        msg_placeholder.markdown(f"""
        <div style='color: #00ff00; font-family: "Courier New"; font-weight: bold;'>
            {random_chars}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(duration)
    
    msg_placeholder.markdown(f"""
    <div style='color: #00ff00; font-family: "Courier New"; font-weight: bold;'>
        {message}
    </div>
    """, unsafe_allow_html=True)
    return msg_placeholder

class ScrapingState:
    def __init__(self):
        self.is_running = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False

def scraping_process(selected_area, platforms, logger, scraping_state):
    try:
        # Validate area first
        area_info = AreaMapping.get_area_info(selected_area)
        if not area_info['is_valid']:
            logger.error(f"Invalid area: {selected_area}")
            suggestions = AreaMapping.suggest_areas(selected_area)
            if suggestions:
                logger.info(f"Did you mean one of these? {', '.join(suggestions)}")
            return [], []

        noon_results = []
        talabat_results = []

        if "Noon" in platforms and scraping_state.is_running:
            if area_info['noon_name']:
                logger.info(f"Starting Noon scraping for {area_info['noon_name']}...")
                noon_results = list(scrape_noon_food(area_info['noon_name']))
            else:
                logger.warning(f"Area '{selected_area}' not available on Noon")

        if "Talabat" in platforms and scraping_state.is_running:
            if area_info['talabat_code']:
                logger.info(f"Starting Talabat scraping for {area_info['noon_name']}...")
                talabat_results = list(scrape_talabat(area_info['talabat_code']))
            else:
                logger.warning(f"Area '{selected_area}' not available on Talabat")

        return noon_results, talabat_results

    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        return [], []

def export_to_csv(noon_results, talabat_results):
    # Create buffer
    buffer = io.StringIO()
    
    # Convert results to dataframes
    if noon_results:
        noon_df = pd.DataFrame(noon_results)
        noon_df['Source'] = 'Noon'
    else:
        noon_df = pd.DataFrame()
        
    if talabat_results:
        talabat_df = pd.DataFrame(talabat_results)
        talabat_df['Source'] = 'Talabat'
    else:
        talabat_df = pd.DataFrame()
    
    # Combine results
    combined_df = pd.concat([noon_df, talabat_df], ignore_index=True)
    
    # Save to buffer
    combined_df.to_csv(buffer, index=False)
    return buffer.getvalue()

def main():
    if 'scraping_state' not in st.session_state:
        st.session_state.scraping_state = ScrapingState()
    
    st.set_page_config(page_title="UAE Restaurant Scraper", layout="wide")
    
    # Matrix-style title
    st.markdown("""
    <h1 style='color: black; font-family: "Courier New"; text-shadow: 0 0 10px #00ff00;'>
        🖥️ UAE Restaurant Matrix
    </h1>
    """, unsafe_allow_html=True)

    # Create Matrix-themed terminal container
    terminal_container = st.empty()
    logger = setup_logger(terminal_container)
    
    # Test logging
    logger.info("Matrix terminal initialized")
    logger.info("System ready for scraping")

    # Get all UAE areas
    all_areas = get_all_uae_areas()
    
    col1, col2 = st.columns([2, 2])
    
    with col1:
        selected_area = st.text_input(
            "Enter Area Name",
            placeholder="e.g., Dubai Marina, Jumeirah, Deira...",
            help="Enter the exact area name as it appears in Noon/Talabat"
        )
        
        # Show area suggestions
        if selected_area:
            suggestions = AreaMapping.suggest_areas(selected_area)
            if suggestions:
                st.info(f"Available areas matching your input: {', '.join(suggestions)}")
            else:
                st.warning(f"No areas found matching '{selected_area}'. Please check the spelling or try another area.")

    with col2:
        platforms = st.multiselect(
            "Select Platforms",
            options=["Noon", "Talabat"],
            default=["Noon", "Talabat"]
        )

    # Create columns for Matrix-themed control buttons
    control_col1, control_col2, control_col3 = st.columns([1, 1, 2])

    with control_col1:
        start_button = st.button("▶ INITIALIZE", type="primary", 
                               disabled=st.session_state.scraping_state.is_running)

    with control_col2:
        stop_button = st.button("⬛ TERMINATE", type="secondary",
                              disabled=not st.session_state.scraping_state.is_running)

    with control_col3:
        clear_button = st.button("⌧ CLEAR LOGS", type="secondary",
                               disabled=st.session_state.scraping_state.is_running)

    if clear_button:
        logger.handlers[0].logs = []
        terminal_container.empty()

    if stop_button:
        logger.warning("TERMINATING SCRAPING SEQUENCE...")
        st.session_state.scraping_state.stop()
        st.session_state.scraping_state = ScrapingState()  # Reset the state
        time.sleep(1)
        st.rerun()

    if start_button:
        st.session_state.scraping_state.start()
        matrix_loading_effect("INITIALIZING SCRAPING SEQUENCE...")
        
        if not st.session_state.scraping_state.is_running:
            return
            
        logger.info("Matrix connection established")
        if not st.session_state.scraping_state.is_running:
            return
            
        logger.info("Accessing restaurant database...")
        logger.info(f"Selected area: {selected_area}")
        logger.info(f"Selected platforms: {', '.join(platforms)}")

        noon_results, talabat_results = scraping_process(
            selected_area, platforms, logger, st.session_state.scraping_state
        )

        if not noon_results and not talabat_results:
            logger.warning("No results found or scraping was interrupted")
            st.session_state.scraping_state.stop()
            st.rerun()
            return

        # Process results (rest of your existing results processing code)
        if noon_results or talabat_results:
            logger.info("Processing results...")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Comparison Table", "Details", "Export"])
            
            with tab3:
                st.subheader("📥 Export Data")
                
                # Create CSV file
                csv_data = export_to_csv(noon_results, talabat_results)
                
                # Add download button
                st.download_button(
                    label="⬇️ Download CSV Report",
                    data=csv_data,
                    file_name=f"restaurant_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                # Show success message
                st.success("CSV file is ready for download!")

        st.session_state.scraping_state.stop()

if __name__ == "__main__":
    main()