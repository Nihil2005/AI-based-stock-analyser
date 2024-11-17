import google.generativeai as genai
import yfinance as yf

from typing import Dict, List
import os


class WealthGeminiAdvisor:
    def __init__(self):
     
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro')

    def get_market_insights(self, symbol: str) -> Dict:
        """Get AI-powered market insights using Gemini for Indian stocks"""
        # Append '.NS' for NSE stocks or '.BO' for BSE stocks
        nse_symbol = f"{symbol}.NS"
        stock = yf.Ticker(nse_symbol)
        try:
            hist = stock.history(period="6mo")
            if hist.empty:
                return {"error": f"No data found for symbol {symbol}"}
        except Exception as e:
            return {"error": str(e)}
        
        #  Indian market specific context
        market_context = f"""
        Stock: {symbol} (NSE)
        Current Price: ₹{hist['Close'].iloc[-1]:.2f}
        6-Month High: ₹{hist['High'].max():.2f}
        6-Month Low: ₹{hist['Low'].min():.2f}
        Volume: {hist['Volume'].iloc[-1]:,}
        """
        
        # Indian market context
        prompt = f"""
        As a financial expert familiar with the Indian stock market, analyze this market data and provide:
        1. Market sentiment considering Indian economic conditions
        2. Key risks including regulatory and market-specific factors
        3. Growth potential in the Indian market context
        4. Investment recommendation considering Indian investor perspective
        
        Data:
        {market_context}
        """
        
        response = self.model.generate_content(prompt)
        return {"insights": response.text}

    def create_wealth_strategy(self, user_data: Dict) -> Dict:
        """Generate personalized wealth building strategy for Indian investors"""
        user_context = f"""
        Profile:
        - Age: {user_data['age']}
        - Income: ₹{user_data['income']:,}
        - Risk tolerance: {user_data['risk_tolerance']}/10
        - Investment goals: {user_data['goals']}
        - Time horizon: {user_data['time_horizon']} years
        """
        
        prompt = f"""
        Create a comprehensive wealth building strategy for this Indian investor:
        {user_context}
        
        Include:
        1. Asset allocation (including Indian equity, debt, and gold)
        2. Investment vehicles (mutual funds, stocks, FDs, PPF, NPS)
        3. Risk management strategy
        4. Tax optimization suggestions under Indian tax laws
        5. Specific action steps for Indian market
        """
        
        response = self.model.generate_content(prompt)
        return {"strategy": response.text}
   
    def get_ai_predictions(self, symbols: List[str]) -> Dict:
        """Get AI predictions for multiple Indian stocks"""
        predictions = {}
        for symbol in symbols:
            nse_symbol = f"{symbol}.NS"
            stock = yf.Ticker(nse_symbol)
            try:
                data = stock.history(period="1y")
                if data.empty:
                    predictions[symbol] = "No data available"
                    continue
            except Exception as e:
                predictions[symbol] = str(e)
                continue
            
            prompt = f"""
            Based on this Indian stock's performance data, provide a 6-month prediction:
            Symbol: {symbol} (NSE)
            Current Price: ₹{data['Close'].iloc[-1]:.2f}
            52-week range: ₹{data['Low'].min():.2f} - ₹{data['High'].max():.2f}
            
            Consider Indian market conditions, economic factors, and potential catalysts.
            """
            
            response = self.model.generate_content(prompt)
            predictions[symbol] = response.text
            
        return predictions


def main():
    advisor = WealthGeminiAdvisor()
    
    # Example usage with Indian context
    user_profile = {
        "age": 30,
        "income": 1500000,  # In INR
        "risk_tolerance": 7,
        "goals": "Build long-term wealth and retire early",
        "time_horizon": 25
    }
    
    # Get personalized strategy
    print("\nFetching wealth strategy...")
    strategy = advisor.create_wealth_strategy(user_profile)
    print("\nStrategy:", strategy)
    
    # Get market insights for specific Indian stocks
    print("\nFetching market insights for Reliance...")
    insights = advisor.get_market_insights("RELIANCE")  # Example with Reliance Industries
    print("\nInsights:", insights)
    
    # Get AI predictions for multiple Indian stocks
    print("\nFetching predictions for multiple stocks...")
    predictions = advisor.get_ai_predictions(["RELIANCE", "TCS", "HDFCBANK"])
    print("\nPredictions:", predictions)


if __name__ == "__main__":
    main()


