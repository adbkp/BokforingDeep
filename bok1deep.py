import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variables
#api_key = os.getenv("OPENROUTER_API_KEY")
api_key="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"
if not api_key:
    st.error("No OpenRouter API key found. Please add it to your .env file as OPENROUTER_API_KEY=your_api_key_here")
    st.stop()

# Initialize OpenAI client with OpenRouter configuration
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
   
)

def get_accounting_advice(transaction_description):
    response = client.chat.completions.create(
        model="google/gemini-2.0-pro-exp-02-05:free",  # Corrected model identifier for OpenRouter
        messages=[
            {"role": "user", "content": f"""Som en mycket erfaren svensk revisor och redovisningskonsult, förklara detaljerat hur följande transaktion ska bokföras enligt svensk redovisningssed och skattelagstiftning:

            Transaktion: {transaction_description}

            Input är beskrivningen av transaktionen som är skriven på svenska.
            
            Analysera mycket noggrant:
            - Transaktionens natur (inköp eller försäljning)
            - Momsskyldighet och korrekt momssats (25%, 12%, 6% eller 0%)
            - Vid försäljning: Utgående moms (debit) ska visas i kreditkolumnen
            - Vid inköp: Ingående moms (kredit) ska visas i debitkolumnen
            - Korrekt momsredovisning enligt svenska regler
            
            Visa bokföringen tydligt i följande format:

            1. Bokföringstabell:
            | Debetkonto (nr och namn) | Debet belopp | Kreditkonto (nr och namn) | Kredit belopp |
            |--------------------------|--------------|---------------------------|---------------|
            | [Kontonr] [Kontonamn]   | [Belopp]    | [Kontonr] [Kontonamn]    | [Belopp]     |

            VIKTIGT: Vid försäljning/intäkt ska utgående moms (konto 2610-2630) visas i kreditkolumnen.
            Vid inköp/kostnad ska ingående moms (konto 2640-2650) visas i debitkolumnen.
            En transaktion kan aldig ha ALDRIG ha både ingående och utgående moms samtidigt.
            VIKTIGT: Var extra noga med att tabellen är helt korrekt och att momsen hanteras på rätt sätt.
            Debet och kredit ska vara korrekt placerade för att bokföringen ska vara rätt.
            Om samma kontonummer förekommer flera gånger i samma kolumn ska beloppen summeras och bara visas en gång. 
            Totalt belopp i kreditkolumnen och totalt belopp i debetkolumnen ska vara lika om konteringen är korrekt.

            2. Utförlig förklaring:
            - Beskriv bokföringen och varför specifika konton används
            - Förklara exakt hur momsen ska hanteras och varför
            - Redogör för eventuella momssatser som är tillämpliga
            - Redovisa särskilda redovisnings- eller momsregler som är relevanta

            3. Viktiga tips:
            - Detaljera viktiga aspekter enligt svenska redovisningsstandarder
            - Påpeka eventuella vanliga fel eller missförstånd
            - Ge konkreta råd om vilken dokumentation som krävs

            Använd alltid konton från den svenska BAS-kontoplanen och ange alltid både kontonummer och kontonamn.
            Var särskilt noggrann med att följa svensk bokföringslag och momslagstiftning. Var också noga med korrekt svenskt språk i svaret."""}
        ]
    )
    return response.choices[0].message.content

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Bokföringshjälpen",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .main {
            background-color: #f7fafc;
            background-image: linear-gradient(45deg, #f7fafc 25%, #edf2f7 25%, #edf2f7 50%, #f7fafc 50%, #f7fafc 75%, #edf2f7 75%, #edf2f7 100%);
            background-size: 56.57px 56.57px;
        }
        .container {
            max-width: 60%;
            margin: 0 auto;
        }
        h1 {
            color: #2b6cb0;
            text-align: center;
        }
        .stButton>button {
            background: linear-gradient(45deg, #2b6cb0, #48bb78);
            color: white;
            border-radius: 25px;
            padding: 0.5em 1em;
            font-size: 1.1em;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        div[data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }
        .advice-container {
            margin-top: 2rem;
            padding: 1.5rem;
            background-color: #f8fafc;
            border-radius: 10px;
            border-left: 4px solid #2b6cb0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a container with 60% width
    st.markdown('<div class="container">', unsafe_allow_html=True)
    
    # Header
    st.title("Bokföringshjälpen")
    st.markdown("<p style='text-align: center;'>Få AI-assisterad vägledning för din bokföring</p>", unsafe_allow_html=True)
    
    # Input section
    st.subheader("Beskriv transaktionen så noggrant som möjligt, för bästa resultat")
    transaction = st.text_area("Transaktionsbeskrivning", placeholder="Exempel: Sålt tjänster för 10 000 kr + moms till ett svenskt företag", height=150)
    
    # Buttons in two columns
    col1, col2 = st.columns([1, 1])
    with col1:
        advice_button = st.button("Få bokföringshjälp", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("Rensa", type="secondary", use_container_width=True)
    
    # Get advice functionality
    if advice_button and transaction.strip():
        with st.spinner("Analyserar transaktion..."):
            advice = get_accounting_advice(transaction)
            st.session_state.advice = advice
            st.rerun()
    elif advice_button and not transaction.strip():
        st.error("Vänligen beskriv transaktionen")
    
    # Show result section below buttons
    if 'advice' in st.session_state:
        st.markdown("<div class='advice-container'>", unsafe_allow_html=True)
        st.subheader("Bokföringsförslag")
        st.markdown(st.session_state.advice)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Clear functionality
    if clear_button:
        if 'advice' in st.session_state:
            del st.session_state.advice
        st.rerun()
    
    # Disclaimer
    st.markdown("""
    <div style='background-color: #fff5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #fc8181; margin-top: 20px;'>
        <h3>⚠️ Viktig information</h3>
        <p>Detta är en AI-genererad vägledning och ska endast användas som hjälpmedel. 
        Konsultera alltid en auktoriserad revisor eller bokföringsexpert för specifika bokföringsfrågor.</p>
        <p>Alla förslag bör verifieras mot aktuella bokföringsregler och BAS-kontoplanen.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Close the container div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
