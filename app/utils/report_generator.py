from typing import Dict, List, Optional
import json
from datetime import datetime
import os
from jinja2 import Environment, FileSystemLoader
import pdfkit
import matplotlib.pyplot as plt
import io
import base64
import logging
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import atexit

class ReportGenerator:
    def __init__(self, template_dir: str = 'app/templates/reports'):
        self.template_dir = template_dir
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.report_dir = 'app/reports'
        self.logger = logging.getLogger(__name__)
        self._ensure_directories()
        
        # Register cleanup
        atexit.register(self._cleanup)
    
    def _cleanup(self):
        """Cleanup resources"""
        plt.close('all')
    
    def _ensure_directories(self):
        """Ensure necessary directories exist"""
        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(os.path.join(self.report_dir, 'html'), exist_ok=True)
        os.makedirs(os.path.join(self.report_dir, 'pdf'), exist_ok=True)
    
    def generate_report(self, 
                       document_info: Dict, 
                       similarity_data: Dict,
                       web_sources: Optional[Dict] = None) -> Dict:
        """Generate comprehensive plagiarism report"""
        try:
            # Generate visualizations
            charts = self._generate_charts(similarity_data)
            
            # Prepare report data
            report_data = {
                'document': document_info,
                'similarity': similarity_data,
                'web_sources': web_sources or {},
                'charts': charts,
                'generated_at': datetime.now().isoformat(),
                'highlighted_text': self._generate_text_highlights(
                    similarity_data.get('detailed_matches', [])
                )
            }
            
            # Generate report in different formats
            report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            html_path = self._save_html_report(report_id, report_data)
            
            # Try to generate PDF, but continue if it fails
            try:
                pdf_path = self._generate_pdf(html_path, report_id)
            except Exception as e:
                self.logger.warning(f"PDF generation failed: {str(e)}")
                pdf_path = None
            
            response = {
                'report_id': report_id,
                'html_path': html_path,
                'summary': self._generate_summary(report_data)
            }
            
            if pdf_path:
                response['pdf_path'] = pdf_path
            
            return response
            
        except Exception as e:
            raise Exception(f"Error generating report: {str(e)}")
    
    def _generate_charts(self, similarity_data: Dict) -> Dict:
        """Generate visualization charts"""
        charts = {}
        
        try:
            # Similarity score distribution
            plt.figure(figsize=(8, 6))
            scores = [
                ('TF-IDF', similarity_data['tfidf_similarity']),
                ('Semantic', similarity_data['semantic_similarity']),
                ('N-gram', similarity_data['ngram_similarity']),
                ('Overall', similarity_data['overall_similarity'])
            ]
            
            plt.bar([s[0] for s in scores], [s[1] for s in scores])
            plt.title('Similarity Scores Distribution')
            plt.ylabel('Similarity Score')
            
            # Convert plot to base64 image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            charts['similarity_distribution'] = base64.b64encode(buffer.read()).decode()
            
        finally:
            plt.close('all')  # Ensure figure is closed
            
        return charts
    
    def _generate_text_highlights(self, matches: List[Dict]) -> List[Dict]:
        """Generate highlighted text comparisons"""
        highlighted_matches = []
        for match in matches:
            highlighted_matches.append({
                'source': match['source_text'],
                'target': match['target_text'],
                'similarity': match['semantic_similarity'],
                'type': 'semantic' if match['semantic_similarity'] > match['levenshtein_similarity']
                        else 'exact'
            })
        return highlighted_matches
    
    def _save_html_report(self, report_id: str, data: Dict) -> str:
        """Generate and save HTML report"""
        template = self.env.get_template('report_template.html')
        html_content = template.render(**data)
        
        html_path = os.path.join(self.report_dir, 'html', f'{report_id}.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return html_path
    
    def _generate_pdf(self, html_path: str, report_id: str) -> str:
        """Generate PDF from HTML report"""
        pdf_path = os.path.join(self.report_dir, 'pdf', f'{report_id}.pdf')
        
        try:
            # Configure PDF options
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': 'UTF-8'
            }
            
            # Try to find wkhtmltopdf in common locations
            wkhtmltopdf_paths = [
                'wkhtmltopdf',  # System PATH
                r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe',  # Windows
                '/usr/local/bin/wkhtmltopdf',  # Unix/Linux
                '/usr/bin/wkhtmltopdf'  # Unix/Linux alternative
            ]
            
            config = None
            for path in wkhtmltopdf_paths:
                if os.path.isfile(path):
                    config = pdfkit.configuration(wkhtmltopdf=path)
                    break
            
            if config:
                pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
            else:
                pdfkit.from_file(html_path, pdf_path, options=options)
            
            return pdf_path
            
        except Exception as e:
            self.logger.error(f"PDF generation failed: {str(e)}")
            raise
    
    def _generate_summary(self, report_data: Dict) -> Dict:
        """Generate report summary"""
        return {
            'document_name': report_data['document']['name'],
            'overall_similarity': report_data['similarity']['overall_similarity'],
            'matched_passages': len(report_data['similarity']['detailed_matches']),
            'generated_at': report_data['generated_at']
        } 
    
    