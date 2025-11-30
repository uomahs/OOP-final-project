import pygame

class SecretAction:
    def __init__(self, name, total_time=10.0, total_hits=10):
        self.name = name                  
        self.is_active = False    
        self.progress = 0.0 # 0.0 ~ 1.0 (게이지 바 그릴 때 사용)
        
        # --- 시간 측정 로직 변수 ---
        self.total_time = total_time      
        self.total_hits = total_hits      
        self.current_hits = 0             
        self.elapsed_acc = 0.0 # 누적 시간    
        self.time_per_hit = 0.2
    
    def start(self, ctx): 
        if not self.is_complete():
            self.is_active = True

    def stop(self, ctx): 
        if self.is_active:
            self.is_active = False 

    def execute(self, dt, ctx): 
        """
        매 프레임 실행되는 핵심 로직
        1. 교수님 감지
        2. 시간 누적 -> 단계 상승 -> 완료 체크
        """
        # 1. 활성화 상태가 아니거나 이미 완료했으면 실행 안 함
        if not self.is_active or self.is_complete():
            return

        # 2. 교수님 감지 ( ctx['professor'] 객체 사용 )
        professor = ctx.get('professor')
        if professor and professor.is_looking_back:
            self.caught(ctx)
            return

        # 3. 시간 누적 및 단계(Hit) 상승 로직
        self.elapsed_acc += dt  # dt(지난 프레임 시간)를 계속 더함
        
        # 누적 시간이 '1단계 시간'을 넘기면 단계 상승
        while self.elapsed_acc >= self.time_per_hit:
            self.elapsed_acc -= self.time_per_hit 
            self.current_hits += 1                
            
        # 4. 진행도 업데이트 (0.0 ~ 1.0) -> UI 게이지용
        self.progress = self.current_hits / self.total_hits

        # 5. 완료 체크
        if self.is_complete():
            self.stop(ctx) # 완료되면 자동으로 멈춤
            print(f" {self.name} 미션 성공!")

    def caught(self, ctx): 
        self.stop(ctx)
        # 걸렸을 때 나타낼 문구 출력
        if 'game' in ctx:
            ctx['game'].set_state('GAME_OVER')

    def is_complete(self):
        return self.progress >= 1.0