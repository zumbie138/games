import pygame

class Botao():
    def __init__(self, x, y, largura, altura, texto, cor_normal, cor_hover):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_atual = cor_normal
        self.clicando = False
        
    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_atual, self.rect)
        pygame.draw.rect(tela, BRANCO, self.rect, 2)
        
        texto_surf = fonte.render(self.texto, True, BRANCO)
        texto_react = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_react)
        
    def verificar_clique(self, evento):
        mouse_pos = pygame.mouse.get_pos()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(mouse_pos):
                self.clicando = True
                return True
        return False
    
    def atualizar(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.cor_atual = self.cor_hover
        else:
            self.cor_atual = self.cor_normal
        self.clicando = False
        
def menu_principal():
    rodando_menu = True
    botao_jogar = Botao(300, 200, 200, 50, 'Jogar', (70, 70, 70), (100, 100, 100))
    botao_sair = Botao(300, 300, 200, 50, 'Sair', (70, 70, 70), (100, 100, 100))
    while rodando_menu:
        tela.fill(PRETO)
        titulo = fonte.render('Demon Exodus', True, BRANCO)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 100))
        
        botao_jogar.atualizar()
        botao_jogar.desenhar(tela)
        botao_sair.atualizar()
        botao_sair.desenhar(tela)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return 'sair'
            if botao_jogar.verificar_clique(evento):
                return 'jogar'
            if botao_sair.verificar_clique(evento):
                return 'sair'
        pygame.display.flip()
        
pygame.init()
fonte = pygame.font.SysFont('Arial', 20)
largura, altura = 1500, 720
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Demon Exodus')
# image = pygame.image.load('D:\games_python\demon_exodus\graph\images\demon_exodus_initial_screen.png').convert()
botao = Botao(300, 400, 200, 50, 'Clique em Mim!', (70, 70, 70), (100, 100, 100))
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

rodando = True

while rodando:
    tela.fill(PRETO)
    # botao.atualizar()
    # botao.desenhar(tela)
    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            rodando = False
        # if botao.verificar_clique(eventos):
        #     print('Botao Clicado !')
    
    opcao = menu_principal()
    if opcao == 'jogar':
        print('jogo começou')
    elif opcao == 'sair':
        rodando = False
    
    # pygame.draw.rect(tela, (255, 0, 0), (100, 100, 50, 50), 0)
    # pygame.draw.circle(tela, BRANCO, (400, 300), 30, 0)
    # pygame.draw.line(tela, (244, 0, 0), (0, 0), (800, 600), 2)
    # tela.blit(image, (0, 0  ))
    pygame.display.flip()
pygame.quit()