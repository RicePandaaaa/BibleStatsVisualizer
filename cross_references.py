import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from collections import defaultdict
from tokens.tokenizer import Tokenizer

def create_chord_diagram():
    """Your original chord diagram function"""
    # Initialize tokenizer
    tokenizer = Tokenizer()
    
    # Create a book-to-book connection matrix
    book_connections = defaultdict(lambda: defaultdict(int))
    
    # Get unique book names
    book_names = list(tokenizer.parsed_verses.keys())
    
    # Count connections between books
    for token_node in tokenizer.token_nodes:
        source_book = token_node.book_name
        
        for reference in token_node.references:
            # Extract book name from reference
            target_book = ' '.join(reference.split(' ')[:-1])
            
            # Only count if it's a different book
            if source_book != target_book and target_book in book_names:
                book_connections[source_book][target_book] += 1
    
    # Create adjacency matrix
    n_books = len(book_names)
    matrix = np.zeros((n_books, n_books))
    
    for i, source_book in enumerate(book_names):
        for j, target_book in enumerate(book_names):
            if source_book in book_connections and target_book in book_connections[source_book]:
                matrix[i][j] = book_connections[source_book][target_book]
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=book_names,
        y=book_names,
        colorscale='Blues',
        text=matrix.astype(int),
        texttemplate='%{text}',
        textfont={"size": 8},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Bible Book Cross-References Heatmap',
        xaxis_title='Referenced Book',
        yaxis_title='Source Book',
        xaxis={'tickangle': -45},
        yaxis={'autorange': 'reversed'},
        width=1200,
        height=1000
    )
    
    return fig

# SOLUTION 1: Save as HTML file and open in browser
def save_and_open_html(fig, filename="bible_visualization.html"):
    """Save the figure as HTML and open it in your default browser"""
    fig.write_html(filename)
    print(f"Saved visualization to {filename}")
    
    # Optionally, automatically open in browser
    import webbrowser
    import os
    webbrowser.open('file://' + os.path.realpath(filename))

# SOLUTION 2: Save as static image
def save_as_image(fig, filename="bible_visualization.png"):
    """Save the figure as a static PNG image"""
    # Note: This requires kaleido to be installed: pip install kaleido
    try:
        fig.write_image(filename, width=1200, height=1000, scale=2)
        print(f"Saved visualization to {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
        print("Make sure you have kaleido installed: pip install kaleido")

# SOLUTION 3: Display in Jupyter Notebook
def display_in_notebook(fig):
    """Display the figure in a Jupyter notebook"""
    # Set the default renderer for notebook
    pio.renderers.default = "notebook"
    fig.show()

# SOLUTION 4: Create a matplotlib version for simpler display
def create_matplotlib_heatmap():
    """Create the same visualization using matplotlib (works in more environments)"""
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Initialize tokenizer
    tokenizer = Tokenizer()
    
    # Create a book-to-book connection matrix
    book_connections = defaultdict(lambda: defaultdict(int))
    
    # Get unique book names
    book_names = list(tokenizer.parsed_verses.keys())
    
    # Count connections between books
    for token_node in tokenizer.token_nodes:
        source_book = token_node.book_name
        
        for reference in token_node.references:
            target_book = ' '.join(reference.split(' ')[:-1])
            
            if source_book != target_book and target_book in book_names:
                book_connections[source_book][target_book] += 1
    
    # Create adjacency matrix
    n_books = len(book_names)
    matrix = np.zeros((n_books, n_books))
    
    for i, source_book in enumerate(book_names):
        for j, target_book in enumerate(book_names):
            if source_book in book_connections and target_book in book_connections[source_book]:
                matrix[i][j] = book_connections[source_book][target_book]
    
    # Create matplotlib figure
    plt.figure(figsize=(20, 16))
    
    # Create heatmap using seaborn
    sns.heatmap(matrix, 
                xticklabels=book_names,
                yticklabels=book_names,
                cmap='Blues',
                cbar_kws={'label': 'Number of References'},
                square=True,
                linewidths=0.1)
    
    plt.title('Bible Book Cross-References Heatmap', fontsize=20, pad=20)
    plt.xlabel('Referenced Book', fontsize=14)
    plt.ylabel('Source Book', fontsize=14)
    plt.xticks(rotation=90, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('bible_heatmap_matplotlib.png', dpi=300, bbox_inches='tight')
    plt.show()

# SOLUTION 5: Print connection statistics instead
def print_connection_stats():
    """Print text-based statistics about the connections"""
    tokenizer = Tokenizer()
    
    # Count connections
    book_connections = defaultdict(lambda: defaultdict(int))
    total_refs_out = defaultdict(int)
    total_refs_in = defaultdict(int)
    
    for token_node in tokenizer.token_nodes:
        source_book = token_node.book_name
        
        for reference in token_node.references:
            target_book = ' '.join(reference.split(' ')[:-1])
            
            if source_book != target_book and target_book in tokenizer.parsed_verses:
                book_connections[source_book][target_book] += 1
                total_refs_out[source_book] += 1
                total_refs_in[target_book] += 1
    
    print("=== TOP 20 MOST REFERENCED BOOKS ===")
    for book, count in sorted(total_refs_in.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{book:25} {count:5} incoming references")
    
    print("\n=== TOP 20 BOOKS WITH MOST OUTGOING REFERENCES ===")
    for book, count in sorted(total_refs_out.items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"{book:25} {count:5} outgoing references")
    
    print("\n=== TOP 20 BOOK-TO-BOOK CONNECTIONS ===")
    all_connections = []
    for source in book_connections:
        for target, count in book_connections[source].items():
            all_connections.append((source, target, count))
    
    for source, target, count in sorted(all_connections, key=lambda x: x[2], reverse=True)[:20]:
        print(f"{source:20} → {target:20} : {count:4} references")

# Main execution with multiple options
if __name__ == "__main__":
    print("Creating visualization...")
    
    # Create the figure
    fig = create_chord_diagram()
    
    # Choose your display method:
    #print("\n=== DISPLAY OPTIONS ===")
    #print("1. Saving as HTML and opening in browser...")
    #save_and_open_html(fig)
    
    #print("\n2. Trying to save as PNG...")
    save_as_image(fig)
    
    #print("\n3. Creating matplotlib version...")
    # Uncomment if you want to use matplotlib instead
    # create_matplotlib_heatmap()
    
    #print("\n4. Printing connection statistics...")
    #print_connection_stats()
    
    # If you're in a specific environment, uncomment the appropriate line:
    # For Jupyter Notebook:
    # display_in_notebook(fig)
    
    # For Google Colab:
    # import plotly.io as pio
    # pio.renderers.default = "colab"
    # fig.show()
    
    # For VS Code:
    # pio.renderers.default = "vscode"
    # fig.show()
    
    # For command line (opens in browser):
    # pio.renderers.default = "browser"
    # fig.show()