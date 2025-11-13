from app.repositories.usuario_repository import UsuarioRepository

if __name__ == '__main__':
    user = UsuarioRepository.get_by_nombre('yromero')
    print('usuario data:', user)
