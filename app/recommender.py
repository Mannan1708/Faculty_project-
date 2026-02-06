import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .database import get_db_connection

class FacultyRecommender:
    def __init__(self):
        self.df = None
        # Expanded academic stop words for cleaner signal
        self.academic_stops = [
            'phd', 'university', 'research', 'professor', 'ma', 'mtech', 'ms', 'btech', 'msc', 
            'diploma', 'thesis', 'institute', 'department', 'technology', 'engineering', 'science',
            'indian', 'international', 'school', 'college'
        ]
        from sklearn.feature_extraction import text
        self.stop_words = list(text.ENGLISH_STOP_WORDS.union(self.academic_stops))
        
        # Capture 1-3 grams to find complex terms like "Data Science" or "Signal Processing"
        self.vectorizer = TfidfVectorizer(
            stop_words=self.stop_words, 
            max_features=10000,
            ngram_range=(1, 3) 
        )
        self.tfidf_matrix = None
        self.feature_names = None
        self.load_data()

    def _clean_text(self, text):
        if not text or str(text).lower() in ['none', 'nan', '<na>', '']:
            return ""
        return str(text).lower().strip()

    def load_data(self):
        """Loads data and builds a weighted TF-IDF matrix."""
        conn = get_db_connection()
        try:
            self.df = pd.read_sql_query("SELECT * FROM faculty", conn)
            if not self.df.empty:
                # Weighted feature engineering
                self.df['processed_spec'] = self.df['specialization'].apply(self._clean_text)
                self.df['processed_edu'] = self.df['education'].apply(self._clean_text)
                self.df['processed_name'] = self.df['name'].apply(self._clean_text)
                
                # Heavy weight on specialization
                self.df['combined_text'] = (
                    (self.df['processed_spec'] + " ") * 4 + 
                    (self.df['processed_edu'] + " ") * 2 + 
                    self.df['processed_name']
                )
                
                self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_text'])
                self.feature_names = self.vectorizer.get_feature_names_out()
                print(f"AI Engine loaded with {len(self.df)} profiles and {len(self.feature_names)} features.")
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            conn.close()

    def _extract_keywords(self, text_idx, top_k=3):
        """Extracts top contributing keywords for a document."""
        if self.tfidf_matrix is None: return []
        row = self.tfidf_matrix[text_idx]
        # Get indices of non-zero elements
        cx = row.tocoo()
        # Sort by score
        tuples = zip(cx.col, cx.data)
        sorted_items = sorted(tuples, key=lambda x: x[1], reverse=True)[:top_k]
        return [self.feature_names[i] for i, score in sorted_items]

    def get_semantic_expertise(self, faculty_id: int, top_n=5):
        """IDEA 1: Semantic Expertise Matcher"""
        if self.df is None: return []
        try:
            target_idx = self.df.index[self.df['id'] == faculty_id].tolist()
            if not target_idx: return []
            
            idx = target_idx[0]
            sim_scores = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
            sim_indices = sim_scores.argsort()[-(top_n+1):-1][::-1]
            
            results = []
            for i in sim_indices:
                if sim_scores[i] > 0.05:
                    item = self.df.iloc[i].to_dict()
                    item['similarity_score'] = round(float(sim_scores[i]), 3)
                    item['matched_keywords'] = self._extract_keywords(i)
                    item['recommendation_type'] = "Expertise"
                    results.append(item)
            return results
        except Exception as e:
            print(f"Error in Semantic: {e}")
            return []

    def get_multidisciplinary_bridge(self, faculty_id: int, top_n=5):
        """IDEA 2: Multidisciplinary Bridge (Different Roles)"""
        if self.df is None: return []
        try:
            target_idx = self.df.index[self.df['id'] == faculty_id].tolist()
            if not target_idx: return []
            
            idx = target_idx[0]
            target_type = self.df.iloc[idx]['faculty_type']
            sim_scores = cosine_similarity(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()
            
            results = []
            # Sort by score descending
            sorted_indices = sim_scores.argsort()[::-1]
            
            for i in sorted_indices:
                if i == idx: continue
                # Must be different faculty type
                if self.df.iloc[i]['faculty_type'] == target_type: continue
                
                if sim_scores[i] > 0.01:
                    item = self.df.iloc[i].to_dict()
                    item['similarity_score'] = round(float(sim_scores[i]), 3)
                    item['matched_keywords'] = self._extract_keywords(i)
                    item['recommendation_type'] = "Collaborator"
                    results.append(item)
                    if len(results) >= top_n: break
            return results
        except Exception as e:
            print(f"Error in Bridge: {e}")
            return []

    def get_subject_specialty_match(self, user_query: str, top_n=5):
        """IDEA 3: Student Goal Alignment"""
        if self.df is None or not user_query: return []
        try:
            query_vec = self.vectorizer.transform([user_query])
            sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            sim_indices = sim_scores.argsort()[-top_n:][::-1]
            
            results = []
            for i in sim_indices:
                if sim_scores[i] > 0.01:
                    item = self.df.iloc[i].to_dict()
                    item['similarity_score'] = round(float(sim_scores[i]), 3)
                    item['matched_keywords'] = self._extract_keywords(i)
                    item['recommendation_type'] = "Goal Match"
                    results.append(item)
            return results
        except Exception as e:
            print(f"Error in Subject Match: {e}")
            return []

recommender = FacultyRecommender()
