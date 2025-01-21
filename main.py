import tkinter as tk

class DangerousWritingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DangerousWritingApp")

        # 화면 크기 가져오기
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # 창 크기 설정
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # 중앙 배치
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # 텍스트 입력 영역
        self.text = tk.Text(self.root, wrap=tk.WORD, font=("Arial", 18))
        self.text.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # 상태 표시 레이블
        self.status = tk.Label(self.root, text="글쓰기를 시작하세요...", font=("Arial", 14))
        self.status.pack(pady=10)

        # 타이머 설정 슬라이더
        self.timer_slider = tk.Scale(self.root, from_=1, to=30, orient=tk.HORIZONTAL,
                                     label="타이머 설정 (초)", font=("Arial", 9))
        self.timer_slider.set(5)  # 기본값 5초
        self.timer_slider.pack(pady=10)

        # 복구 버튼
        self.deleted_text = ""  # 삭제된 텍스트 저장
        self.restore_button = tk.Button(self.root, text="복구", command=self.restore_text, font=("Arial", 12))
        self.restore_button.pack(pady=5)

        # 다크 모드 버튼
        self.dark_mode_button = tk.Button(self.root, text="다크 모드", command=self.toggle_dark_mode, font=("Arial", 12))
        self.dark_mode_button.pack(pady=5)

        # 타이머 초기화
        self.timer = None
        self.warning_timer_id = None
        self.reset_timer()

        # 이벤트 바인딩
        self.text.bind("<Key>", self.on_key_press)

        # 자동 저장 시작
        self.auto_save()

        self.root.mainloop()

    def reset_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
        if self.warning_timer_id:
            self.root.after_cancel(self.warning_timer_id)

        self.status.config(text="계속 글을 써야 텍스트가 유지됩니다!", fg="black")
        timer_value = self.timer_slider.get() * 1000
        self.timer = self.root.after(timer_value, self.clear_text)
        # 경고 타이머 (타이머 종료 3초 전)
        if timer_value > 3000:
            self.warning_timer_id = self.root.after(timer_value - 3000, self.warning_timer)

    def clear_text(self):
        self.deleted_text = self.text.get("1.0", tk.END).strip()  # 텍스트 저장
        self.text.delete("1.0", tk.END)
        self.status.config(text="시간 초과! 텍스트가 삭제되었습니다.", fg="red")

    def restore_text(self):
        if self.deleted_text:
            self.text.insert("1.0", self.deleted_text)  # 텍스트 복구
            self.status.config(text="삭제된 텍스트가 복구되었습니다.", fg="blue")
        else:
            self.status.config(text="복구할 텍스트가 없습니다.", fg="orange")

    def warning_timer(self):
        self.status.config(text="시간이 거의 다 되었습니다!", fg="orange")

    def on_key_press(self, event):
        self.reset_timer()

    def toggle_dark_mode(self):
        if self.root["bg"] == "white":
            self.root.config(bg="black")
            self.text.config(bg="black", fg="white", insertbackground="white")
            self.status.config(bg="black", fg="white")
            self.timer_slider.config(bg="black", fg="white", highlightbackground="white")
            self.dark_mode_button.config(text="라이트 모드", bg="black", fg="white")
        else:
            self.root.config(bg="white")
            self.text.config(bg="white", fg="black", insertbackground="black")
            self.status.config(bg="white", fg="black")
            self.timer_slider.config(bg="white", fg="black", highlightbackground="black")
            self.dark_mode_button.config(text="다크 모드", bg="white", fg="black")

    def auto_save(self):
        with open("autosave.txt", "w", encoding="utf-8") as f:
            f.write(self.text.get("1.0", tk.END).strip())
        self.root.after(60000, self.auto_save)  # 1분마다 호출


if __name__ == "__main__":
    DangerousWritingApp()
