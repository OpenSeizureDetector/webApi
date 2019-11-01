<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\User $user
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('Edit User'), ['action' => 'edit', $user->id]) ?> </li>
        <li><?= $this->Form->postLink(__('Delete User'), ['action' => 'delete', $user->id], ['confirm' => __('Are you sure you want to delete # {0}?', $user->id)]) ?> </li>
        <li><?= $this->Html->link(__('List Users'), ['action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New User'), ['action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Usertypes'), ['controller' => 'Usertypes', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Usertype'), ['controller' => 'Usertypes', 'action' => 'add']) ?> </li>
        <li><?= $this->Html->link(__('List Datapoints'), ['controller' => 'Datapoints', 'action' => 'index']) ?> </li>
        <li><?= $this->Html->link(__('New Datapoint'), ['controller' => 'Datapoints', 'action' => 'add']) ?> </li>
    </ul>
</nav>
<div class="users view large-9 medium-8 columns content">
    <h3><?= h($user->id) ?></h3>
    <table class="vertical-table">
        <tr>
            <th scope="row"><?= __('Uname') ?></th>
            <td><?= h($user->uname) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Email') ?></th>
            <td><?= h($user->email) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Password') ?></th>
            <td><?= h($user->password) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Usertype') ?></th>
            <td><?= $user->has('usertype') ? $this->Html->link($user->usertype->title, ['controller' => 'Usertypes', 'action' => 'view', $user->usertype->id]) : '' ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Id') ?></th>
            <td><?= $this->Number->format($user->id) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Created') ?></th>
            <td><?= h($user->created) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Modified') ?></th>
            <td><?= h($user->modified) ?></td>
        </tr>
    </table>
    <div class="related">
        <h4><?= __('Related Datapoints') ?></h4>
        <?php if (!empty($user->datapoints)): ?>
        <table cellpadding="0" cellspacing="0">
            <tr>
                <th scope="col"><?= __('Id') ?></th>
                <th scope="col"><?= __('DataTime') ?></th>
                <th scope="col"><?= __('User Id') ?></th>
                <th scope="col"><?= __('Wearer Id') ?></th>
                <th scope="col"><?= __('AccMean') ?></th>
                <th scope="col"><?= __('AccSd') ?></th>
                <th scope="col"><?= __('Hr') ?></th>
                <th scope="col"><?= __('Category Id') ?></th>
                <th scope="col"><?= __('DataJSON') ?></th>
                <th scope="col"><?= __('Created') ?></th>
                <th scope="col"><?= __('Modified') ?></th>
                <th scope="col" class="actions"><?= __('Actions') ?></th>
            </tr>
            <?php foreach ($user->datapoints as $datapoints): ?>
            <tr>
                <td><?= h($datapoints->id) ?></td>
                <td><?= h($datapoints->dataTime) ?></td>
                <td><?= h($datapoints->user_id) ?></td>
                <td><?= h($datapoints->wearer_id) ?></td>
                <td><?= h($datapoints->accMean) ?></td>
                <td><?= h($datapoints->accSd) ?></td>
                <td><?= h($datapoints->hr) ?></td>
                <td><?= h($datapoints->category_id) ?></td>
                <td><?= h($datapoints->dataJSON) ?></td>
                <td><?= h($datapoints->created) ?></td>
                <td><?= h($datapoints->modified) ?></td>
                <td class="actions">
                    <?= $this->Html->link(__('View'), ['controller' => 'Datapoints', 'action' => 'view', $datapoints->id]) ?>
                    <?= $this->Html->link(__('Edit'), ['controller' => 'Datapoints', 'action' => 'edit', $datapoints->id]) ?>
                    <?= $this->Form->postLink(__('Delete'), ['controller' => 'Datapoints', 'action' => 'delete', $datapoints->id], ['confirm' => __('Are you sure you want to delete # {0}?', $datapoints->id)]) ?>
                </td>
            </tr>
            <?php endforeach; ?>
        </table>
        <?php endif; ?>
    </div>
</div>
