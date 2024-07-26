class QueuesAnswer:
    @staticmethod
    def get_all_queues_answer(content):
        answer = "Список доступных очередей: \n\n"

        for i in range(len(content)):
            if i != 0:
                answer += "\n\n"
            answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
            answer += content[i]["description"] + "\n"
            answer += "Активно: " + ("Да" if content[i]["active"] else "Нет")

        return answer

    @staticmethod
    def get_active_queues_answer(content):
        answer = "Список активных очередей: \n\n"

        for i in range(len(content)):
            if content[i]["active"]:
                if i != 0:
                    answer += "\n\n"
                answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
                answer += content[i]["description"] + "\n"
        answer += "\n\n"
        answer += "Чтобы активировать очередь, напишите: Активировать *название очереди или ее номер*\n"
        answer += "Чтобы деактивировать очередь, напишите: Деактивировать *название очереди или ее номер*\n"
        return answer

    @staticmethod
    def get_inactive_queues_answer(content):
        answer = "Список неактивных очередей: \n\n"

        for i in range(len(content)):
            if not content[i]["active"]:
                if i != 0:
                    answer += "\n\n"
                answer += str(content[i]["id"]) + ". " + content[i]["name"] + "\n"
                answer += content[i]["description"] + "\n"

        return answer