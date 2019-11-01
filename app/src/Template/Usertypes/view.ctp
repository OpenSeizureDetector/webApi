<?php
/**
 * @var \App\View\AppView $this
 * @var \Cake\Datasource\EntityInterface $usertype
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('Edit Usertype'), ['action' => 'edit', $usertype->id]) ?> </li>
        <li><?= $this->Form->postLink(__('Delete Usertype'), ['action' => 'delete', $usertype->id], ['confirm' => __('Are you sure you want to delete # {0}?', $usertype->id)]) ?> </li>
        <li><?= $this->Html->link(__('List Usertypes'), ['action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Usertype'), ['action' => 'add']) ?> </li>
    </ul>
</nav>
<div class="usertypes view large-9 medium-8 columns content">
    <h3><?= h($usertype->title) ?></h3>
    <table class="vertical-table">
        <tr>
            <th scope="row"><?= __('Title') ?></th>
            <td><?= h($usertype->title) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Description') ?></th>
            <td><?= h($usertype->description) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Id') ?></th>
            <td><?= $this->Number->format($usertype->id) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Created') ?></th>
            <td><?= h($usertype->created) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Modified') ?></th>
            <td><?= h($usertype->modified) ?></td>
        </tr>
    </table>
</div>
