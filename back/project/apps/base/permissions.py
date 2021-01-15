from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Student

class IsInstitutionOwner(UserPassesTestMixin):

    def test_func(self):
        if self.request.user != self.request.user.institution.owner:
            raise PermissionDenied("Você não possui autorização para isto.")
            return False
        return True


class CanHandleStudent(UserPassesTestMixin):

    def test_func(self):
        student = Student.objects.get(id=self.kwargs.get('pk') )
        if student.institution != self.request.user.institution:
            raise PermissionDenied("Você não possui autorização para isto.")
        return True


