from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from .models import Robot, RobotModel
import json



@method_decorator(csrf_exempt, name='dispatch')
class RobotAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            model = data.get('model')
            version = data.get('version')
            created = data.get('created')

            # Validate required fields
            if not all([model, version, created]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Validate model existence
            if not RobotModel.objects.filter(model=model).exists():
                return JsonResponse({"error": "Model does not exist."}, status=400)

            # Check if the robot already exists
            serial = f"{model}-{version}"
            if Robot.objects.filter(serial=serial).exists():
                return JsonResponse({"message": "Robot already exists.", "serial": serial}, status=200)
            
            # Create and save a new Robot instance
            robot = Robot.objects.create(
                model=model,
                version=version,
                created=created
            )

            return JsonResponse({"message": "Robot created successfully.", "serial": robot.serial}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format.", "example": {"model":"A1","version":"V2","created":"2022-12-31 23:59:59"}}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
