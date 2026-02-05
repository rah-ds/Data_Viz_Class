"""
Monthly Reading Summary Generator
=================================

This script generates a monthly summary of O'Reilly reading data including:
- Total time read per month (in minutes and hours)
- Top category of books read each month
- Cumulative total time read

Each highlight represents 20 minutes of reading time.

Author: Ryan Healy
Course: Data Visualization
"""

import pandas as pd
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_FILE = Path(__file__).parent.parent / 'data' / 'oreilly-annotations.csv'
OUTPUT_DIR = Path(__file__).parent.parent / 'data' / 'data_processed'
OUTPUT_FILE = OUTPUT_DIR / 'monthly_reading_summary.csv'
MINUTES_PER_HIGHLIGHT = 20  # Each highlight = 20 minutes of reading

# =============================================================================
# TOPIC CATEGORIZATION
# =============================================================================

def categorize_book(title: str) -> str:
    """
    Categorize books into topic domains based on title keywords.
    
    Parameters:
    -----------
    title : str
        Book title to categorize
        
    Returns:
    --------
    str : Topic category
    """
    if pd.isna(title) or title.strip() == '':
        return 'Other'
    
    title_lower = title.lower()
    
    # AI/Machine Learning
    if any(word in title_lower for word in ['ai ', 'ai engineering', 'machine learning', 'deep learning', 
                                              'neural', 'llm', 'generative', 'reinforcement', 'mlops',
                                              'prompt engineering']):
        return 'AI/ML'
    
    # Statistics/Math
    elif any(word in title_lower for word in ['statistics', 'statistical', 'bayesian', 
                                                'math', 'probability', 'rethinking']):
        return 'Statistics'
    
    # Data Engineering
    elif any(word in title_lower for word in ['data engineering', 'kafka', 'spark', 
                                                'sql', 'database', 'data-intensive']):
        return 'Data Engineering'
    
    # DevOps/Infrastructure
    elif any(word in title_lower for word in ['devops', 'terraform', 'aws', 'azure', 
                                                'jenkins', 'git', 'linux', 'kubernetes']):
        return 'DevOps/Cloud'
    
    # Python/Programming
    elif any(word in title_lower for word in ['python', 'programming', 'flask', 'api', 'recursion']):
        return 'Python/Programming'
    
    # Data Science General
    elif any(word in title_lower for word in ['data science', 'data analysis', 'visualization',
                                               'geospatial']):
        return 'Data Science'
    
    # Algorithms/CS Fundamentals
    elif any(word in title_lower for word in ['algorithm', 'data structure', 'graph']):
        return 'Algorithms/CS'
    
    else:
        return 'Other'


def main():
    """
    Main function to generate monthly reading summary.
    """
    # Load data
    print(f"Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)
    
    # Clean and parse dates
    df['Date of Highlight'] = pd.to_datetime(df['Date of Highlight'], errors='coerce')
    
    # Remove rows with invalid dates
    df = df.dropna(subset=['Date of Highlight'])
    
    # Categorize books
    df['Category'] = df['Book Title'].apply(categorize_book)
    
    # Extract year-month for grouping
    df['Year_Month'] = df['Date of Highlight'].dt.to_period('M')
    
    # Calculate monthly statistics
    monthly_stats = []
    
    for year_month in sorted(df['Year_Month'].unique()):
        month_data = df[df['Year_Month'] == year_month]
        
        # Count highlights (each is 20 min of reading)
        highlight_count = len(month_data)
        time_minutes = highlight_count * MINUTES_PER_HIGHLIGHT
        time_hours = time_minutes / 60
        
        # Find top category for the month
        category_counts = month_data['Category'].value_counts()
        top_category = category_counts.index[0] if len(category_counts) > 0 else 'N/A'
        top_category_count = category_counts.iloc[0] if len(category_counts) > 0 else 0
        top_category_time_min = top_category_count * MINUTES_PER_HIGHLIGHT
        
        monthly_stats.append({
            'year_month': str(year_month),
            'highlight_count': highlight_count,
            'time_read_minutes': time_minutes,
            'time_read_hours': round(time_hours, 2),
            'top_category': top_category,
            'top_category_highlights': top_category_count,
            'top_category_time_minutes': top_category_time_min
        })
    
    # Create summary dataframe
    summary_df = pd.DataFrame(monthly_stats)
    
    # Sort by date (chronological order)
    summary_df = summary_df.sort_values('year_month').reset_index(drop=True)
    
    # Add cumulative total time
    summary_df['cumulative_time_minutes'] = summary_df['time_read_minutes'].cumsum()
    summary_df['cumulative_time_hours'] = round(summary_df['cumulative_time_minutes'] / 60, 2)
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save to CSV
    summary_df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSummary saved to: {OUTPUT_FILE}")
    
    # Display summary
    print("\n" + "="*80)
    print("MONTHLY READING SUMMARY")
    print("="*80)
    print(f"\nEach highlight = {MINUTES_PER_HIGHLIGHT} minutes of reading\n")
    print(summary_df.to_string(index=False))
    
    # Overall statistics
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    total_highlights = summary_df['highlight_count'].sum()
    total_minutes = summary_df['time_read_minutes'].sum()
    total_hours = total_minutes / 60
    print(f"Total highlights: {total_highlights:,}")
    print(f"Total reading time: {total_minutes:,} minutes ({total_hours:.1f} hours)")
    print(f"Date range: {summary_df['year_month'].iloc[0]} to {summary_df['year_month'].iloc[-1]}")
    
    return summary_df


if __name__ == '__main__':
    main()
