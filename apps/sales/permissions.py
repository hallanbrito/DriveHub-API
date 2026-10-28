from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    """
    Permissão que concede acesso exclusivo a usuários autenticados
    com perfil de Gerente (is_staff, is_superuser ou pertencente aos grupos 'Manager'/'Gerente').
    Nenhum usuário anônimo ou vendedor comum tem acesso.
    """
    message = "Acesso negado: operação restrita a gerentes."

    def has_permission(self, request, view) -> bool:
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return user.groups.filter(name__in=["Manager", "Gerente"]).exists()
