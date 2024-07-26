import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pygame
from components.basic_movement_component import BasicMovementComponent

LEFT_BOUNDARY = 10
RIGHT_BOUNDARY = 1000

class EventManagerMock:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, subscriber):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber)

    def post(self, event):
        if event['type'] in self.subscribers:
            for subscriber in self.subscribers[event['type']]:
                subscriber.notify(event)

class TestBasicMovementComponent(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.entity_rect = pygame.Rect(50, 50, 50, 50)
        self.movement_speed = 5
        self.event_manager = EventManagerMock()
        self.component = BasicMovementComponent(self.entity_rect, self.movement_speed, self.event_manager)
        self.player_rect = pygame.Rect(0, 0, 50, 50)

    def test_subscribe_to_events(self):
        self.assertIn('player_attack', self.event_manager.subscribers)
        self.assertIn(self.component, self.event_manager.subscribers['player_attack'])

    def test_move_left(self):
        initial_x = self.entity_rect.x
        self.component.move_left()
        self.assertEqual(self.entity_rect.x, initial_x - self.movement_speed)

    def test_move_right(self):
        initial_x = self.entity_rect.x
        self.component.move_right()
        self.assertEqual(self.entity_rect.x, initial_x + self.movement_speed)

    def test_sync_player_rect(self):
        self.component.sync_player_rect(self.player_rect)
        self.assertEqual(self.player_rect.centerx, self.entity_rect.centerx)

    def test_limits_movements(self):
        self.component.entity_rect.left = LEFT_BOUNDARY - 10
        self.component.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)
        self.assertEqual(self.component.entity_rect.left, LEFT_BOUNDARY)

        self.component.entity_rect.right = RIGHT_BOUNDARY + 10
        self.component.limits_movements(LEFT_BOUNDARY, RIGHT_BOUNDARY)
        self.assertEqual(self.component.entity_rect.right, RIGHT_BOUNDARY)

    def test_notify_attack_start(self):
        event = {'type': 'player_attack', 'state': 'start'}
        self.component.notify(event)
        self.assertEqual(self.component.state, 'attacking')

    def test_notify_attack_end(self):
        event = {'type': 'player_attack', 'state': 'end'}
        self.component.notify(event)
        self.assertEqual(self.component.state, 'idle')

    def test_no_movement_while_attacking(self):
        self.component.state = 'attacking'
        initial_x = self.entity_rect.x

        self.component.update(self.player_rect)
        self.assertEqual(self.entity_rect.x, initial_x)

        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
        self.component.update(self.player_rect)
        self.assertEqual(self.entity_rect.x, initial_x)

        # Limpa os eventos postados para evitar interferência em outros testes
        pygame.event.clear()

    def test_movement_resumes_after_attack(self):
        self.component.state = 'attacking'
        initial_x = self.entity_rect.x
        print(f'State before update: {self.component.state}, entity_rect.x: {self.entity_rect.x}')

        self.component.update(self.player_rect)
        print(f'After update (attacking): {self.component.state}, entity_rect.x: {self.entity_rect.x}')
        self.assertEqual(self.entity_rect.x, initial_x)

        self.component.state = 'idle'
        print(f'State changed to idle: {self.component.state}, entity_rect.x: {self.entity_rect.x}')
        
        # Simula o pressionamento da tecla A
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a}))
        pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_a}))  # Libera a tecla A
        self.component.update(self.player_rect)
        print(f'After update (idle, moving left): {self.component.state}, entity_rect.x: {self.entity_rect.x}')
        self.assertEqual(self.entity_rect.x, initial_x - self.movement_speed)
        
        initial_x = self.entity_rect.x
        
        # Simula o pressionamento da tecla D
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_d}))
        pygame.event.post(pygame.event.Event(pygame.KEYUP, {'key': pygame.K_d}))  # Libera a tecla D
        self.component.update(self.player_rect)
        print(f'After update (idle, moving right): {self.component.state}, entity_rect.x: {self.entity_rect.x}')
        self.assertEqual(self.entity_rect.x, initial_x + self.movement_speed)
        
        pygame.event.clear()

if __name__ == '__main__':
    unittest.main()