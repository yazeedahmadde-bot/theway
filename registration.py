from flask import Blueprint, request, jsonify
import requests
from datetime import datetime
import json
import os

registration_bp = Blueprint('registration', __name__)

@registration_bp.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        
        # Extract user data
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        interest = data.get('interest', '')
        registration_date = datetime.now().isoformat()
        
        # Validate required fields
        if not name or not email:
            return jsonify({'error': 'الاسم والبريد الإلكتروني مطلوبان'}), 400
        
        # Log registration data
        registration_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'interest': interest,
            'registration_date': registration_date
        }
        
        print("=== NEW REGISTRATION ===")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Interest: {interest}")
        print(f"Registration Date: {registration_date}")
        print("========================")
        
        # Send email notification using a webhook service
        email_success = send_email_notification(registration_data)
        
        return jsonify({
            'message': 'تم التسجيل بنجاح',
            'status': 'success',
            'email_sent': email_success
        }), 200
            
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الخادم'}), 500

def send_email_notification(registration_data):
    """
    Send email notification using a webhook service
    """
    try:
        # Use a webhook service like Formspree or similar
        webhook_url = "https://formspree.io/f/xdkogqpv"  # This is a test endpoint
        
        email_content = f"""
        تسجيل جديد في موقع إيقاظ المواهب الفطرية
        
        الاسم: {registration_data['name']}
        البريد الإلكتروني: {registration_data['email']}
        رقم الهاتف: {registration_data.get('phone', 'غير محدد')}
        مجال الاهتمام: {registration_data.get('interest', 'غير محدد')}
        تاريخ التسجيل: {registration_data['registration_date']}
        
        يمكنك التواصل مع المستخدم عبر البريد الإلكتروني المذكور أعلاه.
        """
        
        # Prepare email data
        email_data = {
            'email': 'yazeedahmad.de@gmail.com',
            'subject': 'تسجيل جديد في موقع إيقاظ المواهب',
            'message': email_content,
            '_replyto': registration_data['email'],
            'name': registration_data['name']
        }
        
        # Send via webhook (this is a fallback method)
        # In production, you would use a proper email service
        response = requests.post(
            webhook_url,
            data=email_data,
            headers={'Accept': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print("Email notification sent successfully")
            return True
        else:
            print(f"Email webhook failed with status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error sending email notification: {str(e)}")
        return False

@registration_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'registration'}), 200

@registration_bp.route('/test-email', methods=['POST'])
def test_email():
    """Test email functionality"""
    test_data = {
        'name': 'مستخدم تجريبي',
        'email': 'test@example.com',
        'phone': '123456789',
        'interest': 'اختبار النظام',
        'registration_date': datetime.now().isoformat()
    }
    
    success = send_email_notification(test_data)
    
    return jsonify({
        'message': 'تم اختبار النظام',
        'email_sent': success
    }), 200

