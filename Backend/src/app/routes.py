from flask import BluePrint, request, jsonify, current_app
from src.workflows.immigration_workflow import ImmigrationWorkflow
from src.database.db import DatabasePool


main_bp = BluePrint('main_bp',__name__)

@main_bp.route('/')
def index():
    return jsonify({'statys': 'healthy'})

@main_bp.route('/api/immigration/assess',methods=['POST'])
async def assess_immigration():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        workflow = ImmigrationWorkflow(DatabasePool) 

        result = await workflow.execute(data)
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error while processing request: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500
    


@main_bp.route('/api/immigration/status/<case_id>')
async def get_status(case_id):
    try:
        with DatabasePool.get_cursor(commit=False) as cur:
            cur.execute(
                "SELECT status, metadata FROM cases WHERE id = %s",
                (case_id,)
            )
            result = cur.fetchone()
            
            if not result:
                return jsonify({"error": "Case not found"}), 404
                
            return jsonify({
                "status": result[0],
                "metadata": result[1]
            })
            
    except Exception as e:
        current_app.logger.error(f"Error fetching status: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    
        