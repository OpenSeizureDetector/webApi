<?php
/**
 * @var \App\View\AppView $this
 * @var \App\Model\Entity\Datapoint[]|\Cake\Collection\CollectionInterface $datapoints
 */
?>
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link(__('New Datapoint'), ['action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Users'), ['controller' => 'Users', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New User'), ['controller' => 'Users', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Wearers'), ['controller' => 'Wearers', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Wearer'), ['controller' => 'Wearers', 'action' => 'add']) ?></li>
        <li><?= $this->Html->link(__('List Categories'), ['controller' => 'Categories', 'action' => 'index']) ?></li>
        <li><?= $this->Html->link(__('New Category'), ['controller' => 'Categories', 'action' => 'add']) ?></li>
    </ul>
</nav>
<div class="datapoints index large-9 medium-8 columns content">
    <h3><?= __('Datapoints') ?></h3>
    <table cellpadding="0" cellspacing="0">
        <thead>
            <tr>
                <th scope="col"><?= $this->Paginator->sort('id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('dataTime') ?></th>
                <th scope="col"><?= $this->Paginator->sort('user_id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('wearer_id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('accMean') ?></th>
                <th scope="col"><?= $this->Paginator->sort('accSd') ?></th>
                <th scope="col"><?= $this->Paginator->sort('hr') ?></th>
                <th scope="col"><?= $this->Paginator->sort('category_id') ?></th>
                <th scope="col"><?= $this->Paginator->sort('created') ?></th>
                <th scope="col"><?= $this->Paginator->sort('modified') ?></th>
                <th scope="col" class="actions"><?= __('Actions') ?></th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($datapoints as $datapoint): ?>
            <tr>
                <td><?= $this->Number->format($datapoint->id) ?></td>
                <td><?= h($datapoint->dataTime) ?></td>
                <td><?= $datapoint->has('user') ? $this->Html->link($datapoint->user->id, ['controller' => 'Users', 'action' => 'view', $datapoint->user->id]) : '' ?></td>
                <td><?= $datapoint->has('wearer') ? $this->Html->link($datapoint->wearer->name, ['controller' => 'Wearers', 'action' => 'view', $datapoint->wearer->id]) : '' ?></td>
                <td><?= $this->Number->format($datapoint->accMean) ?></td>
                <td><?= $this->Number->format($datapoint->accSd) ?></td>
                <td><?= $this->Number->format($datapoint->hr) ?></td>
                <td><?= $datapoint->has('category') ? $this->Html->link($datapoint->category->title, ['controller' => 'Categories', 'action' => 'view', $datapoint->category->id]) : '' ?></td>
                <td><?= h($datapoint->created) ?></td>
                <td><?= h($datapoint->modified) ?></td>
                <td class="actions">
                    <?= $this->Html->link(__('View'), ['action' => 'view', $datapoint->id]) ?>
                    <?= $this->Html->link(__('Edit'), ['action' => 'edit', $datapoint->id]) ?>
                    <?= $this->Form->postLink(__('Delete'), ['action' => 'delete', $datapoint->id], ['confirm' => __('Are you sure you want to delete # {0}?', $datapoint->id)]) ?>
                </td>
            </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <div class="paginator">
        <ul class="pagination">
            <?= $this->Paginator->first('<< ' . __('first')) ?>
            <?= $this->Paginator->prev('< ' . __('previous')) ?>
            <?= $this->Paginator->numbers() ?>
            <?= $this->Paginator->next(__('next') . ' >') ?>
            <?= $this->Paginator->last(__('last') . ' >>') ?>
        </ul>
        <p><?= $this->Paginator->counter(['format' => __('Page {{page}} of {{pages}}, showing {{current}} record(s) out of {{count}} total')]) ?></p>
    </div>
</div>
